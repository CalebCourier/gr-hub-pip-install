from guardrails import Guard
from guardrails.hub import GibberishText, RegexMatch
from guardrails.errors import ValidationError


if __name__ == "__main__":
    guard = Guard().use(
        GibberishText()
    ).use(
        RegexMatch("Hello.*")
    )

    res = guard.validate("Hello, World!")
    assert res.validation_passed is True
    print("Guard rightly passed validation: ", res.validated_output)

    try:
        guard.validate("Goodbye, World!")
    except ValidationError as e:
        print("Guard rightly failed validation: ", e)

    
    