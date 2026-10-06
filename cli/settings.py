from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CliSettings(BaseSettings):
    host: str = "http://localhost:8000"
    repeat: int = Field(default=1, ge=1)

    input: str | None = None
    json_input: str | None = Field(default=None, alias="json")
    output: str = "-"

    model_config = SettingsConfigDict(
        cli_parse_args=True,
        cli_prog_name="cache-cli",
        cli_shortcuts={
            "host": "H",
            "repeat": "r",
            "input": "i",
            "json": "j",
            "output": "o",
        },
    )

    @model_validator(mode="after")
    def validate_input(self):
        if bool(self.input) == bool(self.json_input):
            raise ValueError("Provide either --input or --json, but not both")

        return self
