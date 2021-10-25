# SmartApprox

SmartApprox is a framework that determines the configuration of the approximate memory for an application based on previous knowledge that correlates execution features and imprecision tolerance, in the context of Approximate Computing with nondeterministic errors from memory components.

We presented SmartApprox at the [https://www.igscc.org/](12th International Green and Sustainable Computing Conference (IGSC)). See more at https://varchc.github.io/smartapprox/


# Content

This repo contains the implementation of SmartApprox with Learning Models from SciPy.
The Learning Models were configured in "metrics_SmartApprox.py", and the features set in "configuration_SmartApprox.py".

This implementation contains three error scenarios of DRAM process variation based on data extracted from literature. These scenarios comprehends best, median, and worst error probabilities on the voltage scaling of DRAM data array.

# Usage

```shell
python SmartApprox.py <error_scenario>
```
error_scenario can be any of { best, median, worst }. If no error scenario is specified, the median scenario is used.

The Genetic Algorithm (GA) performs a stochastic search for the best subset of features. The GA from our evaluation is implemented at genetic.py. 

The extracted data from our executions are in the [https://docs.python.org/3/library/pickle.html](pickle) format and are available in the directory "reports/".

## [Presentation](#presentation)

*  [Video presentation](https://www.youtube.com/watch?v=9IfxVGTJqBg)

[![Presentation](https://img.youtube.com/vi/9IfxVGTJqBg/0.jpg)](https://www.youtube.com/watch?v=9IfxVGTJqBg)


## [Applications](#applications)

Our evaluation was performed with the applications from https://github.com/VArchC/apps.



## Cite us
```
@INPROCEEDINGS{SmartApprox-IGSC2021,
  author={Jo\~ao {Fabr\'icio Filho} and Isa\'ias Felzmann and Lucas Wanner},
  booktitle={12th International Green and Sustainable Computing Conference (IGSC)}, 
  title={{SmartApprox: learning-based configuration of approximate memories for energy-efficient execution,}}, 
  year={2021}
}
```
[[Download BibTeX]](https://varchc.github.io/bibtex/smartapprox-igsc2021.bib)
