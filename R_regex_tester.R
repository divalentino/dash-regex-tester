
require("stringr",quietly=TRUE)
args = commandArgs(trailingOnly=TRUE)

if (length(args)<2) {
  print(length(args))
  stop("Two arguments must be supplied (text + regex).n", call.=FALSE)
} else {
    text  = args[1]
    regex = args[2]
}

# print("Got tex")
# print(text)
# print("Got regex")
# print(regex)

x <- c(text)
vals <- str_extract_all(x, regex, simplify = TRUE)

for (val in vals) {
    print(val)
}