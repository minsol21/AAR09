# AAR 09_ Task 2 Resubmit

## File Structure

```
|- Plots                   # This directory includes plot results of the codes.
|- general_robot.py        # Code for the general robot.
|- cautious_robot.py       # Code for the cautious robot.
|- adventurous_robot.py    # Code for the adventurous robot.
|- beta_distribution.py    # Code for the beta distribution method.
```

## Code Description

### a) General Robot

Files:
- `general_robot.py`
- `general_robot.png`

In this code, we have 6 tiles in the tile world. Out of a total of 100 steps, we include 30 steps of exploration to prevent our robot from staying at the end of the world while decreasing uncertainty as much as it can. From the plot, we can see that the robot has correctly predicted tiles with almost zero variance.

### b) Adventurous and Cautious Robot

Files:
- `cautious_robot.py`
- `adventurous_robot.py`
- `beta_distribution.py`
- `cautious_robot.png`
- `adventurous_robot.png`
- `adventurous_robot_2.py`

In this code, we implemented adventurous and cautious behaviors for the robots. We used the binomial distribution method to calculate uncertainty. This time, 10% noise is added, as we can see from the slightly higher variance of the mean distribution plot. Although, the mean prediction of tiles is still focused on either 0.0 or 1.0, representing black or white tiles, respectively.

In the cautious robot, we can observe that it tends to explore fewer tiles, sometimes only staying on 2 or 3 out of 6 tiles. On the other hand, the adventurous robot tends to predict at least 5 or all 6 tiles, even though it visits them only a few times.

In both the adventurous and cautious robots, we calculated the uncertainty based on the data collected at the current position. The calculation uses the variance of a binomial distribution, focusing solely on the proportion of white and black counts at the given position.

In `adventurous_robot_2.py`, we tried a different method for calculating uncertainty. This code calculates uncertainty by considering both the current position and its neighboring positions (left and right). It also incorporates an influence by weighting the uncertainties of neighboring positions differently, based on whether the robot is considering moving left or right on the next step, which are the robot's potential movement directions.

### c) Beta Distribution

Files:
- `beta_distribution.py`

In this code, we simulated both adventurous and cautious robots with beta distribution methods, with 0%, 10%, and 40% noise levels. As the beta distribution is implemented, we expected it to be more useful for our prediction, which is estimating the probabilities of whether a tile will be black or white.

As noise increased, the tendency of the mean being focused on either 0.0 (black) or 1.0 (white) decreased, and it slowly moved towards 0.5, representing an undetermined status of the tile color.
