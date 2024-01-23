/*
 * Copyright Concurrent Technologies Corporation 2021
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

use pyo3::create_exception;
use pyo3::prelude::*;

use fapolicy_rules::db::Entry::*;
use fapolicy_rules::db::{Entry, DB};
use fapolicy_rules::error::Error::{MalformedFileMarker, ZeroRulesDefined};
use fapolicy_rules::ops::Changeset;
use fapolicy_rules::parser::parse::StrTrace;
use fapolicy_rules::parser::rule::parse_with_error_message;

#[pyclass(module = "rules", name = "Rule")]
#[derive(Clone)]
pub struct PyRule {
    pub id: usize,
    pub text: String,
    pub origin: String,
    pub info: Vec<PyRuleInfo>,
    pub valid: bool,
}

impl PyRule {
    pub fn new(
        id: usize,
        text: String,
        origin: String,
        info: Vec<(String, String)>,
        valid: bool,
    ) -> Self {
        let info = info
            .iter()
            .map(|(c, m)| PyRuleInfo {
                category: c.clone(),
                message: m.clone(),
            })
            .collect();

        Self {
            id,
            text,
            origin,
            info,
            valid,
        }
    }
}

#[pymethods]
impl PyRule {
    #[getter]
    fn get_id(&self) -> usize {
        self.id
    }

    #[getter]
    fn get_text(&self) -> String {
        self.text.clone()
    }

    #[getter]
    fn get_origin(&self) -> String {
        self.origin.clone()
    }

    #[getter]
    fn get_info(&self) -> Vec<PyRuleInfo> {
        self.info.clone()
    }

    #[getter]
    fn is_valid(&self) -> bool {
        self.valid
    }

    fn __str__(&self) -> PyResult<String> {
        Ok(format!("{}: {}", self.id, self.text))
    }

    fn __repr__(&self) -> PyResult<String> {
        Ok(format!("{}: {}", self.id, self.text))
    }
}

#[pyclass(module = "rules", name = "Info")]
#[derive(Clone)]
pub struct PyRuleInfo {
    pub category: String,
    pub message: String,
}

#[pymethods]
impl PyRuleInfo {
    #[getter]
    fn get_category(&self) -> String {
        self.category.clone()
    }

    #[getter]
    fn get_message(&self) -> String {
        self.message.clone()
    }
}

/// A mutable collection of rule changes
#[pyclass(module = "rules", name = "RuleChangeset")]
#[derive(Default, Clone)]
pub struct PyChangeset {
    rs: Changeset,
}

impl From<Changeset> for PyChangeset {
    fn from(rs: Changeset) -> Self {
        Self { rs }
    }
}

impl From<PyChangeset> for Changeset {
    fn from(py: PyChangeset) -> Self {
        py.rs
    }
}

create_exception!(rust, MalformedMarkerError, pyo3::exceptions::PyException);
create_exception!(rust, NoRulesDefinedError, pyo3::exceptions::PyException);
create_exception!(rust, RuleParsingError, pyo3::exceptions::PyException);

#[pymethods]
impl PyChangeset {
    #[new]
    pub fn new() -> Self {
        PyChangeset::default()
    }

    pub fn get(&self) -> Vec<PyRule> {
        self.rules()
    }

    pub fn rules(&self) -> Vec<PyRule> {
        to_vec(self.rs.get())
    }

    pub fn parse(&mut self, text: &str) -> PyResult<()> {
        match self.rs.set(text.trim()) {
            Ok(_) => Ok(()),
            Err(MalformedFileMarker(lnum, txt)) => Err(MalformedMarkerError::new_err(format!(
                "{}:malformed-file-marker:{}",
                lnum, txt
            ))),
            Err(ZeroRulesDefined) => Err(NoRulesDefinedError::new_err(format!(
                "{:?}",
                ZeroRulesDefined
            ))),
            Err(e) => Err(RuleParsingError::new_err(format!("{:?}", e))),
        }
    }

    pub fn text(&self) -> Option<&str> {
        self.rs.src().map(|s| &**s)
    }
}

#[pyfunction]
fn rule_text_error_check(txt: &str) -> Option<String> {
    match parse_with_error_message(StrTrace::new(txt)) {
        Ok(_) => None,
        Err(s) => Some(s),
    }
}

pub(crate) fn to_vec(db: &DB) -> Vec<PyRule> {
    db.rules()
        .iter()
        .map(|e| {
            let (valid, text, info) = if e.valid {
                if e.msg.is_some() {
                    let w = e.msg.as_ref().unwrap();
                    (true, e.text.clone(), vec![("w".to_string(), w.clone())])
                } else {
                    (true, e.text.clone(), vec![])
                }
            } else {
                let err = e.msg.as_deref().unwrap_or("???");
                (
                    false,
                    e.text.clone(),
                    vec![("e".to_string(), err.to_string())],
                )
            };
            PyRule::new(e.id, text, e.origin.clone(), info, valid)
        })
        .collect()
}

pub(crate) fn to_text(db: &DB) -> String {
    db.iter()
        .fold((None, String::new()), |x, (_, (origin, e))| match x {
            // no origin established yet
            (None, _) => (
                Some(origin.clone()),
                format!("[{}]\n{}", origin, text_for_entry(e)),
            ),
            // same origin as previous
            (Some(last_origin), acc_text) if last_origin == *origin => (
                Some(last_origin),
                format!("{}\n{}", acc_text, text_for_entry(e)),
            ),
            // origin has changed
            (Some(_), acc_text) => (
                Some(origin.clone()),
                format!("{}\n\n[{}]\n{}", acc_text, origin, text_for_entry(e)),
            ),
        })
        .1
}

pub(crate) fn text_for_entry(e: &Entry) -> String {
    match e {
        Invalid { text, .. } => text.clone(),
        InvalidSet { text, .. } => text.clone(),
        ValidRule(r) => r.to_string(),
        ValidSet(s) => s.to_string(),
        RuleWithWarning(r, _) => r.to_string(),
        SetWithWarning(r, _) => r.to_string(),
        e @ Comment(_) => e.to_string(),
    }
}

#[pyfunction]
fn throw_exception(txt: &str) -> PyResult<()> {
    Err(MalformedMarkerError::new_err(format!(
        "malformed-file-marker:{}",
        txt
    )))
}

pub fn init_module(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyRule>()?;
    m.add_class::<PyRuleInfo>()?;
    m.add_class::<PyChangeset>()?;
    m.add_function(wrap_pyfunction!(rule_text_error_check, m)?)?;
    m.add_function(wrap_pyfunction!(throw_exception, m)?)?;
    m.add(
        "MalformedMarkerError",
        py.get_type::<MalformedMarkerError>(),
    )?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::rules::text_for_entry;
    use fapolicy_rules::db::Entry::Comment;

    #[test]
    fn test_comment_prefix() {
        let text = text_for_entry(&Comment("foo".to_string()));
        assert!(text.starts_with('#'));
        assert!(text.ends_with("foo"));
    }
}
