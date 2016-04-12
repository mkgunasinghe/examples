### START ###

# Code to access Phoenix data (http://phoenixdata.org/description). 
# Credit to: "https://github.com/ulfelder" for functions. 

# Need to create 4 functions first, namely, 'build', 'fetch', 'parse', and 'map'.
# Fetch yesterday's event dataset scraped from over 400 sources (around 3,000 obvs)
# using 'fetchPhoenix'
# Build a range of dates using 'buildPhoenix'
# Parse the data using 'parsePhoenix', and then view it on an interactive map depending
# on date range, country/ies, event type, etc.
# EXAMPLES Line 134 onwards

# Load libraries

rm(list=ls())
library(plyr)
library(downloader)
library(maps)
library(leaflet)
library(magrittr)

### Create functions to get Phoenix data

# Fetch Data
fetchPhoenix <- function(date) {
  dateX <- gsub("-", "", date)
  url<-paste0("https://s3.amazonaws.com/openeventdata/current/events.full.", dateX, ".txt.zip")
  file<-paste0("events.full.", dateX, ".txt")
  tmp<-tempfile()
  download(url, tmp)
  Phoenix.Daily<-read.delim(unz(tmp, file), header=FALSE,stringsAsFactors = FALSE)
  names(Phoenix.Daily) <- c("EventID", "Date", "Year", "Month", "Day", "SourceActorFull",
                            "SourceActorEntity", "SourceActorRole", "SourceActorAttribute",
                            "TargetActorFull", "TargetActorEntity", "TargetActorRole",
                            "TargetActorAttribute", "EventCode", "EventRootCode", "QuadClass",
                            "GoldsteinScore", "Issues", "ActionLat", "ActionLong",
                            "LocationName", "GeoCountryName", "GeoStateName", "SentenceID", "URLs",
                            "NewsSources")
  return(Phoenix.Daily)
}

# Build Data

buildPhoenix <- function(start, end) {
  dateset <- seq(as.Date(start), as.Date(end), by="days")
  List <- lapply(dateset, fetchPhoenix)
  DF <- do.call(rbind, List)
  return(DF)
}

# Parse Data

parsePhoenix <- function(data, start="1900-01-01", end=Sys.Date(),
                         country="any", sourcerole="any", targetrole="any", rootcode="any", eventcode="any", issue="any", goldstein="any", quadclass="any") {
  
  DF = data
  DF$Date2 = with(DF, paste(substr(Date, 1, 4), substr(Date, 5, 6), substr(Date, 7, 8), sep="-"))
  DF$Date2 = as.Date(DF$Date2)
  
  # filter by date range
  if (start!="1900-01-01") {
    DF <- DF[which(DF[,"Date2"] >= as.Date(start)),]
  }
  if (end!=Sys.Date()) {
    DF <- DF[which(DF[,"Date2"] <= as.Date(end)),]
  }
  
  # pick country or countries
  if (("any" %in% country)==FALSE) {
    DF <- DF[DF[,"GeoStateName"] %in% country,]
  }
  
  # pick source actor role(s)
  if (("any" %in% sourcerole)==FALSE) {
    DF <- DF[DF[,"SourceActorRole"] %in% sourcerole,]
  }
  
  # pick target actor role(s)
  if (("any" %in% targetrole)==FALSE) {
    DF <- DF[DF[,"TargetActorRole"] %in% targetrole,]
  }
  
  # pick event category or categories
  if (("any" %in% rootcode)==FALSE) {
    DF <- DF[DF[,"EventRootCode"] %in% rootcode,]
  }
  
  # pick quadclass
  if (("any" %in% quadclass)==FALSE) {
    DF <- DF[DF[,"QuadClass"] %in% quadclass,]
  }
  
  # pick event type(s)
  if (("any" %in% eventcode)==FALSE) {
    DF <- DF[DF[,"EventCode"] %in% eventcode,]
  }
  
  # pick goldstein score(s)
  if (("any" %in% goldstein)==FALSE) {
    DF <- DF[DF[,"GoldsteinScore"] %in% goldstein,]
  }
  
  # pick issue(s)
  List <- strsplit(gsub(";", ",", DF$Issues), split=",")
  Index <- sapply(1:nrow(DF), function(x) as.logical(issue %in% List[[x]]))
  if (("any" %in% issue)==FALSE) {
    DF <- DF[which(Index),]
  }
  
  DF$Date2 <- NULL
  return(DF)
  
}

# Map Data (Can change cluster setting, map tile, popup desc)

mapPhoenix <- function(PhoenixData) {
  
  PhoenixData <- PhoenixData[is.na(PhoenixData[,"ActionLat"])==FALSE,] # drop rows with no geocoordinates
  lmap <- leaflet(PhoenixData) %>%
          addProviderTiles("Stamen.Toner") %>%
          addCircleMarkers(lng = PhoenixData[,"ActionLong"], lat = PhoenixData[,"ActionLat"],
                           popup = paste(PhoenixData[,"Date"], PhoenixData[,"SourceActorFull"], PhoenixData[,"TargetActorFull"], PhoenixData[,"URLs"], sep = " "),
                          stroke = TRUE,  clusterOptions = markerClusterOptions()
                           ) %>%
  print(lmap)
}

#######

# EXAMPLES

X <- fetchPhoenix(Sys.Date()-1) # Fetch yesterday dataset
summary(X)
head(X, 2) # Get the top two observations to understand the data
count(X, 'GeoStateName') # Check how many times a specific state has been mentioned (useful to highlight areas of particular interest)
count(X, 'Issues') # Check if any 'issues' are more salient in a period of time
# mapPhoenix(X) - if you want to map ALL observations for that individual day

X <- buildPhoenix("2016-03-08", "2016-03-12") # Build a dataset of range 08/03/2016 - 12/03/2016 ~ 4 days (17,000 obs)
X2 <- parsePhoenix(X, country="THA", start = "2016-03-10", end ="2016-03-11") # Parse the 4 day range for observations on "Thailand" in reduced date range 10/03 - 11/03 (32 obs))
mapPhoenix(X2) # Visually explore the recorded observations for Thailand in the 2 day range 

# if you want to save txt file on folder instead of tmp:
# download(paste0("https://s3.amazonaws.com/openeventdata/current/events.full.", dateX, ".txt.zip"), dest=paste0("/Users/Documents/", dateX, ".zip"), mode="wb", cacheOK=TRUE) 
# Phoenix<-unzip(paste0("/Users/Documents/", dateX, ".zip"), exdir = "/Users/Documents/")
# Phoenix.Daily<-read.delim(Phoenix, header=FALSE,stringsAsFactors = FALSE)

### END ###
