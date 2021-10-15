# Testing on Sandbox

## Usage

This script can be used to quickly test builds or TEAL apps on sandbox. First, make sure you are running sandbox, change the path to your sandbox in `sandbox-testing.py` and run the following:

```python3 sandbox-testing.py```

### Changing configs

Sandbox can be run on different configs. You can see them in the sandbox directory, as they start with `config.`, e.g. `config.nightly`. You can specify a config by the suffix, e.g. `./sandbox up nightly`.

If you want to test sandbox on an experimental build, make sure the config file points to the appropriate repo and branch.