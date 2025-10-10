library(jsonlite)
library(dplyr)
library(ggplot2)
library(lubridate)
library(hms)

library(sf) # geospatial data wrangling
library(leaflet)

setwd("//Users//VihaanVajpayee//Desktop//Purdue Acedemics//Senior Year Semester One//CS 441//project_folder//brewingcorrelations")

df <- read.csv("data/processed/starbucks_reviews_flat.csv")


length(unique(df$user_id))
length(unique(df$business_id))

########## Visualization Tools ##########
plot_density <- function(df,
                         x_variable, 
                         x_axis_name,
                         categorical_variable = NULL, 
                         color_map = NULL, 
                         x_breaks = NULL, 
                         x_limits = NULL, 
                         cumulative = FALSE,
                         hide_legend = TRUE, 
                         plotname = "density_plot.png", 
                         dimensions = c(6, 3)) {
  x_sym <- sym(x_variable)
  if (!is.null(categorical_variable)) {
    cat_sym <- sym(categorical_variable)
    p <- ggplot(df, aes(x = !!x_sym, color = !!cat_sym))
  } else {
    p <- ggplot(df, aes(x = !!x_sym))
  }
  
  if (cumulative) {
    p <- p + stat_ecdf(geom = "line")
    y_axis_name <- "Cumulative Density"
  } else {
    p <- p + geom_density()
    y_axis_name <- "Density"
  }
  
  p <- p +
    labs(
      title = "", 
      x = x_axis_name, 
      y = y_axis_name
    ) +
    theme_minimal() +
    theme(plot.title = element_blank(),
          axis.title = element_blank(),
          axis.title.x = element_text(size=11, margin=margin(t=15), color = "black"),
          axis.title.y = element_text(size=11, margin=margin(r=15), color = "black"),
          axis.text.x = element_text(size=11, color = "black"),
          axis.text.y = element_text(size=11, color = "black"),
          legend.text = element_text(size=11, color = "black"), 
          legend.title = element_text(size=11, color = "black"), 
          strip.text = element_text(size=11, color = "black"), 
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank(), 
          panel.border = element_rect(color = "black", fill = NA),
          axis.line = element_line(color = "black"), 
          axis.ticks = element_line(color = "black"), 
          text = element_text(family = "serif"))
  
  if (!is.null(color_map) & !is.null(categorical_variable)) {
    p <- p + scale_color_manual(values = color_map)
  }
  
  if (!is.null(x_breaks) & !is.null(x_limits)) {
    p <- p + scale_x_continuous(breaks = x_breaks,
                                limits = x_limits,
                                expand = c(0, 0))
  } else {
    p <- p + scale_x_continuous(expand = c(0, 0))
  }
  
  if (hide_legend) {
    p <- p + theme(legend.position = "none")
  }
  
  ggsave(filename = paste0("plots/", plotname), plot = p,
         width = dimensions[1], height = dimensions[2], dpi = 300, bg = "white")
  
  p
}


############ Visualizations ###########
# Distribution of numerical data
plot_density(
  df = business_sf, 
  x_variable = "avg_rating", 
  x_axis_name = "Star Rating",
  categorical_variable = NULL
)


############### Map of Ratings #################
business_sf <- df %>%
  rename(
    lat = business_latitude, 
    lon = business_longitude,
    star_rating = business_stars
  ) %>%
  group_by(business_id, lat, lon) %>%   # group by business and location
  summarise(avg_rating = mean(star_rating, na.rm = TRUE)) %>%
  ungroup() %>%
  filter(!is.na(lat), !is.na(lon)) %>%
  st_as_sf(coords = c("lon", "lat"), crs = 4326, remove = FALSE) %>%
  mutate(rating_flag = if_else(avg_rating > 3, "avg > 3", "avg ≤ 3"))

# two-color palette
pal <- colorFactor(
  palette = c("forestgreen", "firebrick"),
  domain  = c("avg > 3", "avg ≤ 3")
)

leaflet(business_sf, options = leafletOptions(zoomControl = TRUE)) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  addCircleMarkers(
    lng = ~lon, lat = ~lat,
    color = "black",
    radius = 5, stroke = FALSE, fillOpacity = 0.85,
    label = ~paste0(
      "Business: ", business_id,
      "<br>Avg rating: ", round(avg_rating, 2)
    ),
    labelOptions = labelOptions(direction = "auto")
    # For clustering, uncomment:
    # , clusterOptions = markerClusterOptions()
  ) %>%
  # Continental US view; for AK/HI use fitBounds(-170, 18, -65, 72)
  fitBounds(lng1 = -125, lat1 = 24, lng2 = -66.9, lat2 = 49)



# Distribution of business review count
plot_density(
  df = df, 
  x_variable = "business_review_count", 
  x_axis_name = "Review Count",
  categorical_variable = NULL
)

library(stringr)
df <- df %>%
  mutate(word_count = str_count(text, "\\S+"))

plot_density(
  df = df, 
  x_variable = "word_count", 
  x_axis_name = "Word Count of Review", 
  x_breaks = seq(0, 250, 50), 
  x_limits = c(0, 260)
)


df_business <- df %>%
  group_by(business_id) %>%
  slice(1) %>%
  ungroup()

df_business %>%
  count(business_attributes.RestaurantsPriceRange2) %>%                                  # counts
  mutate(percentage = 100 * n / sum(n)) %>%               # relative freq
  mutate(percentage = sprintf("%.2f%%", percentage)) %>%  # format with %
  select(business_attributes.RestaurantsPriceRange2, percentage)


freq_table <- function(column_name) {
  col_sym <- sym(column_name)
  df_business %>%
    count(!!col_sym) %>%                                  # counts
    mutate(percentage = 100 * n / sum(n)) %>%               # relative freq
    mutate(percentage = sprintf("%.2f%%", percentage)) %>%  # format with %
    select(!!col_sym, percentage)
}

freq_table("business_attributes.WiFi")





