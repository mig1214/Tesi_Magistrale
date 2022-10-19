library(readr)
library(dbplyr)
library(tbl_df)

packages <- c("wordcloud", "tm")

lapply(packages, require , character.only = TRUE)

#all_functions <- read_delim("C:/Users/migue/Desktop/Universita/Magistrale/2_anno/Tesi/Tesi_Magistrale/functions/all_functions.txt",";", escape_double = FALSE, trim_ws = TRUE)
all_patches <- read_delim("D:/all_patches.txt", 
                          ";", escape_double = FALSE, trim_ws = TRUE)

function_text <- Corpus(VectorSource(all_patches))

function_text_clean <- tm_map(function_text, removePunctuation)
function_text_clean <-  tm_map(function_text_clean, content_transformer(tolower))
function_text_clean <-  tm_map(function_text_clean, stripWhitespace)
function_text_clean <- tm_map(function_text_clean, removeWords, stopwords("english"))

wordcloud(function_text, scale = c(2,1), min.freq = 20, colors = c("red", "blue", "green"))
  
