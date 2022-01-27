import championBuilds as cb
import cv2

LolBuildClass = cb.LolBuildScraper()
image = LolBuildClass.getBuild()

cv2.imshow('Lol Build', image)
cv2.waitKey()
