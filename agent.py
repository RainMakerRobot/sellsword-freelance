name: Run Job Agent

on:
  schedule:
    - cron: "0 16 * * *"  # daily
  workflow_dispatch:

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - run: pip install requests beautifulsoup4 openai

      - run: python agent.py
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          EMAIL_USER: ${{ secrets.EMAIL_USER }}
          EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
