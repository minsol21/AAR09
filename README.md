# AAR 09_ Task 2 Resubmit

## File structure
|- Plots
 
 : this file includes plot results of the codes.
|- general_robot.py

|- cautious_robot.py

|- adventurous_robot.py

|- beta_distribution.py

## Code Description
### a) General robot
|- general_robot.py
|- general_robot.png
In this code, we have 6 tiles in the tile world. Out of total 100 steps, we include 30 steps of exploration to predict our robot from staying at the end of the world while decreasing uncertainty as much as it can. From the plot, we can see that robot has correctly predicted tiles with almost 0 variance.

 
 ### b) Adventurous and Cautious robot
|- cautious_robot.py

|- adventurous_robot.py

|- beta_distribution.py

|- cautious_robot.py

|- adventurous_robot.png

|- adventurous_robot_2.py

In this code, we implemented adventurous and cautious behavior of robots. We used binomial distribution method to calculate uncertainty. But this time, 10% noise is added as we can see from a little bit higher variance of the mean distribution plot. Although, the mean of prediction of tile is still focused on either 0.0 or 1.0 which each mean black or white tile. 
In cautious robot, we can observe that it tends to explore less number of tile as it sometime only stay 2 or 3 out of 6 tiles. On the other hand, in adventurous robot, it tends to predict at least 5 or all 6 of them even though it visit a few times.

In both adventurous and cautious robot, we calculated the uncertainty based on the data collected at a current position. The calculation uses the variance of a binomial distribution, focusing solely on the proportion of white and black counts at the given position.

In ``adventurous_robot_2.py`` file, we tried different method for calculating uncertainty. This code calculates uncertainty by considering both the current position and its neighboring positions (left and right). It also incorporates a influence by weighting the uncertainties of neighboring positions differently, based on whether the robot is considering moving left or right on next step, which is robot's potential movement directions.

 ### c) Beta Distribution
|- beta_distribution.py

In this code, we simulated both adventurous robot and cautious robot with beta distribution methods, with 0, 10, 40% noise each. As the beta distribution is implemented, we expected that it will be more useful for our prediction, which is estimating probabilities of whether it will be black or white tile.
Also, as noise was increased, the tendency of mean being focused either 0.0 (black) or 1.0 (white) has decreased, and slowly moving to 0.5, which is undetermined status of color of tile.
