# py_urn_randomizer

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/TavoloPerUno/py_urn_randomizer/actions/workflows/lint.yml/badge.svg)](https://github.com/TavoloPerUno/py_urn_randomizer/actions/workflows/lint.yml)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-informational.svg)](https://tavoloperuno.github.io/py_urn_randomizer/)

A clinical trial urn randomization system implementing the adaptive biased coin
design described by Wei (1978). The system ensures treatment-group balance
according to one or more prognostic factors and exposes its functionality through
a Flask web GUI, a REST API, and a command-line interface.

## Key Features

- **Urn randomization** per Wei (1978) adaptive biased coin design
- **Flask web GUI** with interactive Bokeh plots for monitoring assignments
- **REST API** for programmatic access to randomization services
- **Command-line interface (CLI)** for scripting and batch operations
- **Plugin system** for custom randomization logic
- **Reproducible RNG** via NumPy PCG64 generator
- **SQLite storage** for portable, zero-configuration persistence

## Quick Start

```bash
# Clone the repository
git clone https://github.com/TavoloPerUno/py_urn_randomizer.git
cd py_urn_randomizer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config-sample.yaml config.yaml
# Edit config.yaml to define treatments, factors, and urn parameters

# Set required environment variables (see example.env)
cp example.env .env
# Edit .env with your Google OAuth credentials and secret key

# Initialize the database and create an admin user
flask createdb
flask add_user admin admin@example.com

# Run the application
flask run
```

## CLI Usage

The `urn` command provides direct access to randomization from the terminal.

```bash
# Randomize a participant
urn -s "Study Name" randomize --id P001 -u admin
```

## API Usage

### List study participants

```bash
curl -X GET "http://localhost:5000/study_participants?api_key=YOUR_KEY&study=Study+Name"
```

### Randomize a new participant

```bash
curl -X POST "http://localhost:5000/study_participants?api_key=YOUR_KEY&study=Study+Name&id=P001&factor1=level1&factor2=level2"
```

## Configuration

All study parameters are defined in `config.yaml`. Key settings include:

| Parameter        | Description                                                        |
|------------------|--------------------------------------------------------------------|
| `treatments`     | List of treatment arms (e.g., `[A, B]`)                            |
| `factors`        | Prognostic factors and their levels used for stratification         |
| `w`              | Initial number of balls per treatment in the urn                    |
| `alpha`          | Number of balls added for the assigned treatment after each draw    |
| `beta`           | Number of balls added for the unassigned treatment after each draw  |
| `D`              | Imbalance tolerance parameter                                      |
| `urn_selection`  | Method for selecting among strata urns                              |
| `starting_seed`  | Seed for the NumPy PCG64 random number generator (reproducibility)  |

## Documentation

Full documentation is available on
[GitHub Pages](https://tavoloperuno.github.io/py_urn_randomizer/).

## Citation

If you use this software in your research, please cite the original method:

> Wei, L.J. (1978). The Adaptive Biased Coin Design for Sequential Experiments.
> *Annals of Statistics*, 6(1), 92-100.

## License

This project is licensed under the Apache License 2.0. See the
[LICENSE](LICENSE) file for details.
