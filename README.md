# Tracking GuardrailsAI Hub Validators as Pip Dependencies

## Setup

1. Create a virtual environment

```sh
python -m venv ./.venv
source ./.venv/bin/activate
```

2. Make sure you have a guardrails token/api key set to GUARDRAILS_TOKEN

```sh
echo $GUARDRAILS_TOKEN
```

3. If not,

You can use the one from the .guardrailsrc file that is created when you run `guardrails configure`:

```sh
export GUARDRAILS_TOKEN=$(cat ~/.guardrailsrc| awk -F 'token=' '{print $2}' | awk '{print $1}' | tr -d '\n')
```

Or you can get a new key from the hub at https://hub.guardrailsai.com/keys


4. Setup pip environment variables

```sh
export PIP_INDEX_URL="https://__token__:$GUARDRAILS_TOKEN@pypi.guardrailsai.com/simple"
export PIP_TRUSTED_HOST="pypi.guardrailsai.com pypi.org"
export PIP_EXTRA_INDEX_URL="https://pypi.org/simple"
```

5. Install requirements

```sh
pip install .
```

6. Run hub install to perform post-install actions.  Since the pip packages are already installed, it will skip that step and only perform post-install unless you specify the `--upgrade` flag.

```sh
guardrails hub install hub://guardrails/gibberish_text hub://guardrails/regex_match
```

7. Run the test

```sh
python test.py
```


## Identifying Package Names for Guardrails Hub Validators
At the time of writing this (Feb 19, 2025), the package names in Guardrails' private pypi index are formed as follows:

Given a hub url in the form of:
`hub://{namespace}/{validator_name}`
 
the package name in the private index will be:
`{namespace}-grhub-{validator_name}`

Examples:
1. `hub://guardrails/gibberish_text` -> `guardrails-grhub-gibberish-text`
2. `hub://tryolabs/restricttotopic` -> `tryolabs-grhub-restricttotopic`


## Notes on Future Improvement
We're looking at better ways to manage hub installs as we work towards an official 1.x.  The toil associated with hub installs is top of mind and we plan to streamline this process as much as possible.