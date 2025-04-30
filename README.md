# Tracking GuardrailsAI Hub Validators as Pip Dependencies

## As of guardrails-ai v0.6.x
To comment on this as whole, the first thing to note is that hub validators are not just code.  Many of them also have ML models that back them.  The reason the guardrails cli exists at all (wrt to installing from the hub) is because there are post install actions that need to occur to make the validators more usable (i.e. downloading backing models & weights, setting up barrel files for easier imports, etc.).  Some, but not all, of this, like downloading model weights, can and will happen at runtime if post install is not run, but this takes a non-trivial amount of time hence the install-time hook instead.

There are ways to install the underlying pip packages themselves using only pip, but this will not run the post-install.  One workaround is to install the pip packages first, then run the hub install command afterwards.  As long as you don't pass the update flag to the hub install, it will see that the packages are already installed and only run post-install.  This still requires an API key because the packages themselves are in a private pypi registry that requires authentication.

This workaround is what the code sample in this repo covers.

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


4. Setup pip env vars

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