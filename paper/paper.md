---
title: 'Python Finite Volume Solid Mechanics Solver'
tags:
- Python
- Solid Mechanics
- Finite Volume Method
- Linear Elastic
- ANOTHER
authors:
- name: Scott Levie
  orcid: 0000-0002-4302-5887
  affiliation: 2
- name: Philip Cardiff
  orcid: xxxx-xxxx-xxxx-xxxxx
  affiliation: "1, 2"
affiliations:
- name: University College Dublin
  index: 1
- name: IRC?
  index: 2
date: 01 April 2022
bibliography: paper.bib
---

# Summary

This learning framework is a set of Jupyter notebooks that provide an in-dept explanation of each step required to build a working solid mechanics solver, these include: governing equations derivation; finite-difference and finite-volume discretisation of governing equations; implementation of fixed displacement and fixed traction boundary conditions; and segregated solution algorithm techniques. 

**INSERT LIST OF NOTEBOOK TITLES**

The series the functions and classes created in each notebook form a 2-dimensional linear-elastic implicit segregated solid solver for a rectangular structured mesh, which is capable of applying either fixed displacement or fixed traction boundary conditions. The same functions and classes are also laid out in a separate directory to allow for an accessible solver for problem solving capabilities.

# Statement of need

The Finite Volume (FV) method techniques for Computational Solid Mechanics (CSM) is an emerging alternative to the widely used (FE) method; in some cases, it has been shown to be faster than commercial FE software [1]. Solids4foam [2] is an open-source toolbox for solid mechanics and fluid-solid interactions that uses the FV framework within OpenFOAM, traditionally used for CFD. While solids4foam is a powerful tool for CSM it lacks a certain accessibility, especially to those with limited computer science skills. The aim of this work is to provide an easily accessible open-source tool that requires little effort and time to run, which can be used in both a problem solving and educational capacity. 

# Validation of Solver

INSERT PIECE COMPARING SOLVER TO S4F

# Acknowledgements


# References