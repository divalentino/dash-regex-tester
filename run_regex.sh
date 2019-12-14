#!/bin/bash

default_text="The patient was admitted on 12-JAN-2019 and died on 16-JAN-2019"
default_regex="([[:digit:]]{2}-)?(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-[[:digit:]]{2}([[:digit:]]{2})?"

Rscript --vanilla R_regex_tester.R "${1:-${default_text}}" "${2:-${default_regex}}"