# ConvertQC - Mapping Quantum Circuits Between Different Environments

## Introduction
This repository contains the source code and final report for my dissertation, ConvertQC, submitted as partial fulfillment of a BSc (Hons) in Computer Science, eventually graduating with a 2nd Class Upper Honours.

The aim of this project is to translate scripts from various quantum computing and technologies simulators into different formats. Currently, the script is able to work between ProjectQ and QuTiP, with future work hopefully coming soon.

Before any major work begins, however, I aim to greatly refactor this project. In short - i'm displeased with it. The code is poor and doesn't do the best job of translation, requiring a lot of user checking and edits. I'd like to explore the abstract syntax trees used by Python, and use this to translate the scripts. The alternative is to create a central XML-based format which is simpler to translate in and out of.

## Installation

Clone the repository, and run 

`python3 setup.py`

## File Structure

### /examples/

Contains example scripts available for translating, both ProjectQ and QuTiP

### /package/

Contains source code for ConvertQC

### /report/

Contains details for the technical report such as figures and sources.

## Contact

If you have any queries or concerns, please email me at convertqc@gmail.com
