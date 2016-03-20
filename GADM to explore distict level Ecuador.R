### START ###

# Using GADM to explore district level Ecuador map ##

# Load libraries

library(rgdal)
library(raster)
library(sp)
library(rgeos)
library(RColorBrewer)

# Load the shape files
getData("ISO3") # Find 3 character country name
ecuador<-getData('GADM', country="ECU", level=1)

# Function to reduce amount of space for each polygon on GADM database
# Get the main polygons determined by area
getSmallPolys <- function(poly, minarea=0.01) {
  # Get the areas
  areas <- lapply(poly@polygons, 
                  function(x) sapply(x@Polygons, function(y) y@area))
  
  # Figure out big polygons
  bigpolys <- lapply(areas, function(x) which(x > minarea))
  length(unlist(bigpolys))
  
  # Keep only the big polygons
  for(i in 1:length(bigpolys)){
    if(length(bigpolys[[i]]) >= 1 && bigpolys[[i]][4] >= 1){
      poly@polygons[[i]]@Polygons <- poly@polygons[[i]]@Polygons[bigpolys[[i]]]
      poly@polygons[[i]]@plotOrder <- 1:length(poly@polygons[[i]]@Polygons)
    }
  }
  return(poly)
}
# End of Function

# EXAMPLES

# Get polygon data for district level Ecuador
ecuador <- getData('GADM', country="ECU", level=1)

# Look at data **(not able if space reducing function is applied)** - find out variables of interest
ecuador@data

# Apply function to reduce virtual space
ecuador <- gSimplify(ecuador, tol=0.01, topologyPreserve=TRUE)

# Provide a background color for regions
colors <- rep("grey", 24)

# Shade other regions in another color if necessary
colors[2] <- "red" # Bolivar Province 
colors[8] <- "red" # Esmeraldas Province 
colors[18] <- "red" # Pastaza Province 

# Plotting the map
plot(ecuador, col = colors, border = 'black', main = "Example of Ecuador Map")

# Set font of district names on map **(not able if space reducing function is applied)**
invisible(text(getSpPPolygonsLabptSlots(ecuador), labels=as.character(ecuador$NAME_1), cex=0.4))

# City level

# Focusing on a individual district in Ecuador (instead of whole country) ##
ecuador2 <- getData('GADM', country="ECU", level=2)

# Look at data **(not able if space reducing function is applied)** - find out variables of interest
ecuador2@data

# Apply function to reduce virtual space
ecuador2 <- gSimplify(ecuador2, tol=0.01, topologyPreserve=TRUE)

# Focusing on the region of Bolivar
# Get city level data only if in district of Bolivar **(not able if space reducing function is applied)**
bolivar = (ecuador2[ecuador2$NAME_1=="Bolivar",])

# Look at data **(not able if space reducing function is applied)** - find out variables of interest
bolivar@data

# Apply function to reduce virtual space
bolivar <- gSimplify(bolivar, tol=0.01, topologyPreserve=TRUE)

# Provide a background color for cities in region
colors2 <- rep("grey", 7)

# Shade cities in another color if necessary
colors2[1] <- "red" # City of Caluma
colors2[6] <- "red" # City of Las Naves
colors2[7] <- "red" # City of San Miguel

# Plotting the map
plot(bolivar, col = colors2, border = 'black', main = "Example of Bolivar Province")

# Set font of city names on map **(not able if space reducing function is applied)**
invisible(text(getSpPPolygonsLabptSlots(bolivar), labels=as.character(bolivar$NAME_2), cex=0.4))

### END ###

# Clear environment
rm(list=ls())
