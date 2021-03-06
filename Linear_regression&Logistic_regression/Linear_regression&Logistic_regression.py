# -*- coding: utf-8 -*-
"""hw2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rNOj-2WuOVBhEELFy_F5dGSs_oaKpL_9

# CS171-EE142 - Fall 2021 - Homework 2

# Due: Friday, October 29, 2021 @ 11:59pm

### Maximum points: 100 pts

## Submit your solution to Gradescope:
1. Submit screenshot images or a single PDF to **HW2**
2. Submit your jupyter notebook to **HW2-code**

**Important**: 

1. Please make sure that the submitted notebook has been run and the outputs are visible. **If the output is not visible, you will lose points.**

2. Make sure the LaTeX math is properly rendered for PDF. **Check this [link](https://docs.google.com/presentation/d/1UBWMyyNzqcPiaN-yMzoqD3-0GkjHVQr-m_A1qnfQIa8/edit?usp=sharing) for instructions on how to easily convert ipynb to PDF.**

3. In Markdown, when you write in LaTeX math mode, do not leave space after the first dollar sign ($). For example, write `$\mathbf{w}$` instead of `$(space)\mathbf{w}$`. Otherwise, nbconvert will throw an error and the generated pdf will be incomplete. [This is a bug of nbconvert.](https://tex.stackexchange.com/questions/367176/jupyter-notebook-latex-conversion-fails-escaped-and-other-symbols)

### Enter your information below:

<div style="color: #000000;background-color: #EEEEFF">
    Your Name (submitter): Hsiangwei Hsiao <br> 
    Your student ID (submitter): 862254811
    
<b>By submitting this notebook, I assert that the work below is my own work, completed for this course.  Except where explicitly cited, none of the portions of this notebook are duplicated from anyone else's work or my own previous work.</b>
</div>

## Academic Integrity
Each assignment should be done  individually. You may discuss general approaches with other students in the class, and ask questions to the TAs, but  you must only submit work that is yours . If you receive help by any external sources (other than the TA and the instructor), you must properly credit those sources, and if the help is significant, the appropriate grade reduction will be applied. If you fail to do so, the instructor and the TAs are obligated to take the appropriate actions outlined at http://conduct.ucr.edu/policies/academicintegrity.html . Please read carefully the UCR academic integrity policies included in the link.

# Overview 
In this assignment you will implement and test two supervised learning algorithms: linear regression (Problem 1) and logistic regression (Problem 2). 

For this assignment we will use the functionality of Pandas (https://pandas.pydata.org/), Matplotlib (https://matplotlib.org/), and Numpy (http://www.numpy.org/). You may also find Seaborn (https://seaborn.pydata.org/) useful for some data visualization.

If you are asked to **implement** a particular functionality, you should **not** use an existing implementation from the libraries above (or some other library that you may find). When in doubt, please ask. 

Before you start, make sure you have installed all those packages in your local Jupyter instance


## Read *all* cells carefully and answer all parts (both text and missing code)

You will complete all the code marked `TODO` and answer descriptive/derivation questions
"""

import random as rand

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split 

# make sure you import here everything else you may need

"""## Question 1: Linear Regression [70 pts]
We will implement linear regression using direct solution and gradient descent. 

We will first attempt to predict output using a single attribute/feature. Then we will perform linear regression using multiple attributes/features. 

### Getting data
In this assignment we will use the Boston housing dataset. 

The Boston housing data set was collected in the 1970s to study the relationship between house price and various factors such as the house size, crime rate, socio-economic status, etc.  Since the variables are easy to understand, the data set is ideal for learning basic concepts in machine learning.  The raw data and a complete description of the dataset can be found on the UCI website:

https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.names
https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data

or 

http://www.ccs.neu.edu/home/vip/teach/MLcourse/data/housing_desc.txt

I have supplied a list `names` of the column headers.  You will have to set the options in the `read_csv` command to correctly delimit the data in the file and name the columns correctly.
"""

names =[
    'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 
    'AGE',  'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'PRICE'
]

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/housing/housing.data',
                 header=None,delim_whitespace=True,names=names,na_values='?')

df.head()

"""### Basic Manipulations on the Data

What is the shape of the data?  How many attributes are there?  How many samples?
Print a statement of the form:

    num samples=xxx, num attributes=yy

In order to properly test linear regression, we first need to find a set of correlated variables, so that we use one to predict the other. Consider the following scatterplots:
"""

sb.pairplot(df[['RM','LSTAT','PRICE']])

"""Create a response vector `y` with the values in the column `PRICE`.  The vector `y` should be a 1D `numpy.array` structure."""

# TODO 
y = np.array(df['PRICE'])
y.shape

"""Use the response vector `y` to find the mean house price in thousands and the fraction of homes that are above $40k. (You may realize this is very cheap.  Prices have gone up a lot since the 1970s!).   Create print statements of the form:

    The mean house price is xx.yy thousands of dollars.
    Only x.y percent are above $40k.
"""

# TODO 
y.mean()
print("The mean house price is {:.2f} thosusands of dollars.".format(y.mean()))
len(y)
count = 0
for i in y:
  if i > 40:
    count += 1
# print(count)
percent = count/len(y)*100
# print(percent)
print("Only {:.1f} percent are above $40k.".format(percent))

"""### Visualizing the Data

Python's `matplotlib` has very good routines for plotting and visualizing data that closely follows the format of MATLAB programs.  You can load the `matplotlib` package with the following commands.
"""

# Commented out IPython magic to ensure Python compatibility.
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline

"""Similar to the `y` vector, create a predictor vector `x` containing the values in the `RM` column, which represents the average number of rooms in each region."""

# TODO
x = np.array(df['RM'])
x

"""Create a scatter plot of the price vs. the `RM` attribute.  Make sure your plot has grid lines and label the axes with reasonable labels so that someone else can understand the plot."""

# TODO
fig, ax = plt.subplots()
ax.scatter(x,y)
ax.grid()
ax.set_title("Price V.S Room")
ax.set_xlabel("Room(unit)")
ax.set_ylabel("Price($K)")

"""The number of rooms and price seem to have a linear trend, so let us try to predict price using number of rooms first.

### Question 1a. Derivation of a simple linear model for a single feature [10 pts]
Suppose we have $N$ pairs of training samples $(x_1,y_1),\ldots, (x_N,y_N)$, where $x_i \in \mathbb{R}$ and $y_i \in \mathbb{R}$. 

We want to perform a linear fit for this 1D data as 
$$y = wx+b,$$
where $w\in \mathbb{R}$ and $b\in \mathbb{R}$. 

In the class, we looked at the derivation of optimal value of $w$ when $b=0$. The squared loss function can be written as  $$L(w) = \sum_{i=1}^N(w x_i -y_i)^2,$$ and the optimal value of $w*$ that minimizes $L(w)$ can be written as $$w^* = (\sum_{i=1}^N x_i^2)^{-1}(\sum_{i=1}^N x_i y_i)$$. 


Now let us include $b$ in our model. Show that the optimal values of $w^*,b^*$ that minimize the loss function 
$$L(w,b) = \sum_{i=1}^N(wx_i + b -y_i)^2$$ 
can be written as 
$$w^* = (\sum_i (x_i - \bar{x})^2)^{-1}(\sum_i (x_i-\bar{x})(y_i-\bar{y}))$$
and $$b^* = \bar{y} - w^*\bar{x},$$
where $\bar{x} = \frac{1}{N}\sum_i x_i, \bar{y} = \frac{1}{N}\sum_i y_i$ are mean values of $x_i,y_i$, respectively.

**TODO: Your derivation goes here.**

The partial differential $w$ for the partial derivative of loss function:

$$\frac{\partial L(w,b)}{\partial w} = 2\sum_{i=1}^N x_i(w'x_i' + b -y_i)$$

With respect to $w$ and $b$ equal to zero, the partial derivative can be rewritten as:

$$\frac{\partial L(w,b)}{\partial w} = 2\sum_{i=1}^N x_i(w'x_i' -y_i)$$

The partial differential $b$ for the partial derivative of loss function:

$$\frac{\partial L(w,b)}{\partial b} = 2\sum_{i=1}^N (w'x_i' + b -y_i)$$


With respect to $w$ and $b$ equal to zero, the partial derivative can be rewritten as:

$$\frac{\partial L(w,b)}{\partial b} = 2\sum_{i=1}^N (w'x_i' -y_i)$$


*   *Hint. Set the partial derivative of $L(w,b)$ with respect to $w$ and $b$ to zero.*
*   Type using latex commands and explain your steps

### Question 1b. Fitting a linear model using a single feature [10 pts] 

Next we will write a function to perform a linear fit. Use the formulae above to compute the parameters $w,b$ in the linear model $y = wx + b$.
"""

def fit_linear(x,y):
    """
    Given vectors of data points (x,y), performs a fit for the linear model:
       yhat = w*x + b, 
    The function returns w and b
    """
    # TODO complete the code below
    x_mean = np.array(df['RM']).mean()
    y_mean = np.array(df['PRICE']).mean()
    sum_num = 0
    sum_deno = 0;
    for i in range(len(x)):
      sum_num += (x[i]-x_mean)*(y[i]-y_mean)
      sum_deno += pow((x[i]-x_mean),2)

    w = sum_num/sum_deno
    b = y_mean - w*(x_mean)
    return w,b
print(fit_linear(x,y))

"""Using the function `fit_linear` above, print the values `w`, `b` for the linear model of price vs. number of rooms."""

# TODO
w, b = fit_linear(x,y)
print('w = {0:5.1f}, b = {1:5.1f}'.format(w,b))

"""Does the price increase or decrease with the number of rooms? 

* *Your answer here*

The price increase with the number of rooms.

Replot the scatter plot above, but now with the regression line.  You can create the regression line by creating points `xp` from say min(x) to max(x), computing the linear predicted values `yp` on those points and plotting `yp` vs. `xp` on top of the above plot.
"""

import random
# TODO
# Points on the regression line
xp = []
np.array(xp)
for i in np.arange(min(x), max(x),0.01):
  xp.append(i)
print(xp)

yp = []
np.array(yp)
for m in xp:
  yp.append(m*w + b)
print(yp)

fig, ax = plt.subplots()
ax.scatter(x,y)
ax.scatter(xp,yp)
ax.grid()
ax.set_title("Price V.S Room")
ax.set_xlabel("Room(unit)")
ax.set_ylabel("Price($K)")

"""### Question 1c. Linear regression with multiple features/attributes [20 pts]
One possible way to try to improve the fit is to use multiple variables at the same time.

In this exercise, the target variable will be the `PRICE`.  We will use multiple attributes of the house to predict the price.  

The names of all the data attributes are given in variable `names`. 
* We can get the list of names of the columns from `df.columns.tolist()`.  
* Remove the last items from the list using indexing.
"""

xnames = names[:-1]
print(names[:-1])

"""Let us use `CRIM`, `RM`, and `LSTAT` to predict `PRICE`. 

Get the data matrix `X` with three features (`CRIM`, `RM`, `LSTAT`) and target vector `y` from the dataframe `df`.  

Recall that to get the items from a dataframe, you can use syntax such as

    s = np.array(df['RM'])  
        
which gets the data in the column `RM` and puts it into an array `s`.  You can also get multiple columns with syntax like

    X12 = np.array(df['CRIM', 'ZN'])  

"""

# TODO
#    X = ...
#    y = ...
X = np.array(df[['CRIM', 'RM', 'LSTAT']])
Y = np.array(df['PRICE'])

"""**Linear regression in scikit-learn**

To fit the linear model, we could create a regression object and then fit the training data with regression object.

```
from sklearn import linear_model
regr = linear_model.LinearRegression()
regr.fit(X_train,y_train)
```

You can see the coefficients as
```
regr.intercept_
regr.coef_
```

We can predict output for any data as 

    y_pred = regr.predict(X)

**Instead of taking this approach, we will implement the regression function directly.**

**Linear regression by solving least-squares problem (direct solution)**

Suppose we have $N$ pairs of training samples $(x_1,y_1),\ldots, (x_N,y_N)$, where $\mathbf{x}_i \in \mathbb{R}^d$ and $y_i \in \mathbb{R}$. 

We want to perform a linear fit over all the data features as 
$$y = \mathbf{\tilde w}^T\mathbf{x}+b,$$
where $\mathbf{\tilde w}\in \mathbb{R}^d$ and $b\in \mathbb{R}$. 

We saw in the class that we can write all the training data as a linear system 
$$ \begin{bmatrix} y_1 \\ \vdots \\ y_N \end{bmatrix} = \begin{bmatrix} - & \mathbf{x}_1^T & - \\ 
& \vdots & \\
- & \mathbf{x}_N^T& - \end{bmatrix} \mathbf{\tilde w} + b, $$
which can be written as 
$$ \begin{bmatrix} y_1 \\ \vdots \\ y_N \end{bmatrix} = \begin{bmatrix} 1 & \mathbf{x}_1^T \\ 
\vdots & \vdots \\
1 & \mathbf{x}_N^T\end{bmatrix} \begin{bmatrix} b \\ \mathbf{\tilde w} \end{bmatrix}.$$

Let us write this system of linear equations in a compact form as 
\begin{equation} 
\mathbf{y} = \mathbf{X}\mathbf{w}, 
\end{equation} 
where $\mathbf{X}$ is an $N \times d+1$ matrix whose first column is all ones and $\mathbf{w}$ is a vector of length $d+1$ whose first term is the constant and rest of them are the coefficients of the linear model. 

The least-squares problem for the system above can be written as 
$$\text{minimize}\; \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2$$
for which the closed form solution can be written as 
$$\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.$$

**Append ones to the data matrix**

To compute the coefficients $\mathbf{\tilde w}$, we first append a vector of ones to the data matrix.  This can be performed with the `ones` command and `hstack`.  Note that after we do this, `X` will have one more column than before.
"""

# TODO  
# your code here 
X = np.hstack([np.ones([X.shape[0], 1]), X])
X

"""**Split the Data into Training and Test**

Split the data into training and test.  Use 30% for test and 70% for training.  You can do the splitting manually or use the `sklearn` package `train_test_split`.   Store the training data in `Xtr,ytr` and test data in `Xts,yts`.

"""

from sklearn.model_selection import train_test_split

# TODO 
# your code here 
Xtr, Xts, ytr, yts = train_test_split(X, Y, test_size=0.3)

"""Now let us compute the coefficients $\mathbf{w}$ using `Xtr,ytr` via the direct matrix inverse: $$\mathbf{w} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.$$

You may use `np.linalg.inv` to compute the inverse. For a small problem like this, it makes no difference.  But, in general, using a matrix inverse like this is *much* slower computationally than using functions such as `lstsq` method or the `LinearRegression` class.  In real world, you will never solve a least squares problem like this. 
"""

# TODO
# compute w using the direct solution equation 
XT_X = np.dot((Xtr.transpose()), Xtr)

XT_X_1 = np.linalg.inv(XT_X)
X_result = np.dot(XT_X_1, Xtr.transpose())
w = np.dot(X_result, ytr)

"""Compute the predicted values `yhat_tr` on the training data and print the average square loss value on the training data."""

# TODO 
# your code here 
yhat_tr = np.dot(Xtr, w)
yhat_tr
squared_loss = 0
for i in range(len(yhat_tr)):
  squared_loss += pow((yhat_tr[i] - ytr[i]),2)
ave_squared_loss = squared_loss/len(yhat_tr)

print("Average square loss value is", ave_squared_loss)

"""Create a scatter plot of the actual vs. predicted values of `y` on the training data."""

# TODO 
# your code here 
fig, ax = plt.subplots()
ax.scatter(ytr, yhat_tr)

ax.grid()
ax.set_title("Actual values y V.S Predicted values y")
ax.set_xlabel("Actual values")
ax.set_ylabel("Predicted values")

"""Compute the predicted values `yhat_ts` on the test data and print the average square loss value on the test data."""

# TODO 
# your code here 
yhat_ts = np.dot(Xts, w)
squared_loss = 0
for i in range(len(yhat_ts)):
  squared_loss += pow((yhat_ts[i] - yts[i]),2)
ave_squared_loss = squared_loss/len(yhat_ts)

print("Average square loss value is", ave_squared_loss)

"""Create a scatter plot of the actual vs. predicted values of `y` on the test data."""

# TODO 
# your code here 
fig, ax = plt.subplots()
ax.scatter(yts, yhat_ts)

ax.grid()
ax.set_title("Actual values y V.S Predicted values y")
ax.set_xlabel("Actual values")
ax.set_ylabel("Predicted values")

"""### Question 1d: Gradient descent for linear regression [20 pts]
Finally, we will implement the gradient descent version of linear regression.

In particular, the function implemented should follow the following format:
```python
def linear_regression_gd(X,y,learning_rate = 0.00001,max_iter=10000,tol=pow(10,-5)):
```
Where `X` is the same data matrix used above (with ones column appended), `y` is the variable to be predicted, `learning_rate` is the learning rate used ($\alpha$ in the slides), `max_iter` defines the maximum number of iterations that gradient descent is allowed to run, and `tol` is defining the tolerance for convergence (which we'll discuss next).

The return values for the above function should be (at the least) 1) `w` which are the regression parameters, 2) `all_cost` which is an array where each position contains the value of the objective function $L(\mathbf{w})$ for a given iteration, 3) `iters` which counts how many iterations did the algorithm need in order to converge to a solution.

Gradient descent is an iterative algorithm; it keeps updating the variables until a convergence criterion is met. In our case, our convergence criterion is whichever of the following two criteria happens first:

- The maximum number of iterations is met
- The relative improvement in the cost is not greater than the tolerance we have specified. For this criterion, you may use the following snippet into your code:
```python
np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol
```

Gradient can be computed as $$\nabla_\mathbf{w}L = \mathbf{X}^T(\mathbf{X}\mathbf{w} - \mathbf{y}).$$

Estimate will be updated as $\mathbf{w} \gets \mathbf{w} - \alpha \nabla_\mathbf{w}L$ at every iteration. 

**Note that the $\mathbf{w}$ in this derivation includes the constant term and $\mathbf{X}$ is a matrix that has ones column appended to it.**
"""

# TODO 
# Implement gradient descent for linear regression 

def compute_cost(X,w,y):
    # your code for the loss function goes here 
    predict = X.dot(w)
    m = len(y)
    # L = (1/2*m) * np.sum(np.square(predict-y))
    L = np.sum(np.square(predict-y))
    return L

def linear_regression_gd(X,y,learning_rate = 0.00001,max_iter=10000,tol=pow(10,-5)):

# your code goes here
  w = np.random.randn(4,1)
  m = len(y)
  all_cost = np.zeros(max_iter)
  iters = 0;
  for it in range(max_iter):
    prediction = np.dot(X,w)
    w = w -learning_rate*( X.T.dot((prediction - y)))
    # w = w -(1/m)*learning_rate*( X.T.dot((prediction - y)))
    all_cost[it] = compute_cost(X,w,y)
    iters += 1
    if np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol:
      break
      
  return w, all_cost, iters

"""### Question 1e: Convergence plots [10 pts]
After implementing gradient descent for linear regression, we would like to test that indeed our algorithm converges to a solution. In order see this, we are going to look at the value of the objective/loss function $L(\mathbf{w})$ as a function of the number of iterations, and ideally, what we would like to see is $L(\mathbf{w})$ drops as we run more iterations, and eventually it stabilizes. 

The learning rate plays a big role in how fast our algorithm converges: a larger learning rate means that the algorithm is making faster strides to the solution, whereas a smaller learning rate implies slower steps. In this question we are going to test two different values for the learning rate:
- 0.00001
- 0.000001

while keeping the default values for the max number of iterations and the tolerance.


- Plot the two convergence plots (cost vs. iterations) [5]

- What do you observe? [5]

<b>Important</b>: In reality, when we are running gradient descent, we should be checking convergence based on the <i>validation</i> error (i.e., we would have to split our training set into e.g., 70/30 training'/validation subsets, use the new training set to calculate the gradient descent updates and evaluate the error both on the training set and the validation set, and as soon as the validation loss stops improving, we stop training. <b>In order to keep things simple, in this assignment we are only looking at the training loss</b>, but as long as you have a function 
```python
def compute_cost(X,w,y):
```
that calculates the loss for a given X, y, and set of parameters you have, you can always compute it on the validation portion of X and y (that are <b>not</b> used for the updates).  
"""

# TODO 
# test gradient descent with step size 0.00001
# test gradient descent with step size 0.000001

(w, all_cost,iters) = linear_regression_gd(Xtr,ytr,learning_rate = 0.00001,max_iter = 1000, tol=pow(10,-6))  
print(iters)
plt.figure(0)
plt.title('Linear regression_gd for step size 0.00001')
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss')  
# complete the rest

(w, all_cost,iters) = linear_regression_gd(Xtr,ytr,learning_rate = 0.000001,max_iter = 1000, tol=pow(10,-6))  

plt.figure(0)
plt.title('Linear regression_gd for step size 0.000001')
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss')

"""Observations: 

1. How fast to find the optimal $w$ depends on learning rate. Bigger learning rate is much faster.
1. The training loss is getting small during iteration.

### Question 2. Logistic regression [30 pts]

In this question, we will plot the logistic function and perform logistic regression. We will use the breast cancer data set.  This data set is described here:

https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin

Each sample is a collection of features that were manually recorded by a physician upon inspecting a sample of cells from fine needle aspiration.  The goal is to detect if the cells are benign or malignant.  

We could use the `sklearn` built-in `LogisticRegression` class to find the weights for the logistic regression problem.  The `fit` routine in that class has an *optimizer* to select the weights to best match the data.  To understand how that optimizer works, in this problem, we will build a very simple gradient descent optimizer from scratch.

### Loading and visualizing the Breast Cancer Data

We load the data from the UCI site and remove the missing values.
"""

names = ['id','thick','size_unif','shape_unif','marg','cell_size','bare',
         'chrom','normal','mit','class']
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/' +
                 'breast-cancer-wisconsin/breast-cancer-wisconsin.data',
                names=names,na_values='?',header=None)
df = df.dropna()
df.head(6)

"""After loading the data, we can create a scatter plot of the data labeling the class values with different colors.  We will pick two of the features.  """

# Get the response.  Convert to a zero-one indicator 
yraw = np.array(df['class'])
BEN_VAL = 2   # value in the 'class' label for benign samples
MAL_VAL = 4   # value in the 'class' label for malignant samples
y = (yraw == MAL_VAL).astype(int)
Iben = (y==0)
Imal = (y==1)

# Get two predictors
xnames =['size_unif','marg'] 
X = np.array(df[xnames])

# Create the scatter plot
plt.plot(X[Imal,0],X[Imal,1],'r.')
plt.plot(X[Iben,0],X[Iben,1],'g.')
plt.xlabel(xnames[0], fontsize=16)
plt.ylabel(xnames[1], fontsize=16)
plt.ylim(0,14)
plt.legend(['malign','benign'],loc='upper right')

"""The above plot is not informative, since many of the points are on top of one another.  Thus, we cannot see the relative frequency of points.

### Logistic function

We will build a binary classifier using *logistic regression*.  In logistic regression, we do not just output an estimate of the class label.  Instead, we ouput a *probability*, an estimate of how likely the sample is one class or the other.  That is our output is a number from 0 to 1 representing the likelihood:
$$
    P(y = 1|x)
$$
which is our estimate of the probability that the sample is one class (in this case, a malignant sample) based on the features in `x`.  This is sometimes called a *soft classifier*.  

In logistic regression, we assume that likelihood is of the form
$$
    P(y=1|x) = \sigma(z),  \quad z = w(1)x(1) + \cdots + w(d)x(d) + b = \mathbf{w}^T\mathbf{x}+b,  
$$
where $w(1),\ldots,w(d),b$ are the classifier weights and $\sigma(z)$ is the so-called *logistic* function:
$$
    \sigma(z) = \frac{1}{1+e^{-z}}.
$$

To understand the logistic function, suppose $x$ is a scalar and samples $y$ are drawn with $P(y=1|x) = f(w x+b)$ for some $w$ and $b$.  We plot these samples for different $w,b$.
"""

N = 100
xm = 20
ws = np.array([0.5,1,2,10])
bs = np.array([0, 5, -5])
wplot = ws.size
bplot = bs.size
iplot = 0
for b in bs: 
  for w in ws:
    iplot += 1
    x  = np.random.uniform(-xm,xm,N)
  
    py = 1/(1+np.exp(-w*x-b))
 
    yp = np.array(np.random.rand(N) < py) # hard label for random points
    xp = np.linspace(-xm,xm,100) 
    pyp = 1/(1+np.exp(-w*xp-b)) # soft label (probability) for the points

    plt.subplot(bplot,wplot,iplot)

    plt.scatter(x,yp,c=yp,edgecolors='none',marker='+')
    plt.plot(xp,pyp,'b-')
    plt.axis([-xm,xm,-0.1,1.1])
    plt.grid() 
    if ((iplot%4)!=1):
        plt.yticks([])
    plt.xticks([-20,-10,0,10,20])
    plt.title('w={0:.1f}, b={1:.1f}'.format(w,b))

    plt.subplots_adjust(top=1.5, bottom=0.2, hspace=0.5, wspace=0.2)

"""We see that $\sigma(wx+b)$ represents the probability that $y=1$.  The function $\sigma(wx) > 0.5$ for $x>0$ meaning the samples are more likely to be $y=1$.  Similarly, for $x<0$, the samples are more likely to be $y=0$.  The scaling $w$ determines how fast that transition is and $b$ influences the transition point.

### Fitting the Logistic Model on Two  Variables

We will fit the logistic model on the two variables `size_unif` and `marg` that we were looking at earlier.
"""

# load data 
xnames =['size_unif','marg'] 
X = np.array(df[xnames])
print(X.shape)

"""Next we split the data into training and test"""

# Split into training and test
from sklearn.model_selection import train_test_split
Xtr, Xts, ytr, yts = train_test_split(X,y, test_size=0.30)

"""**Logistic regression in scikit-learn**

The actual fitting is easy with the `sklearn` package.  The parameter `C` 
states the level of inverse regularization strength with higher values meaning less regularization. Right now, we will select a high value to minimally regularize the estimate.

We can also measure the accuracy on the test data. You should get an accuracy around 90%. 
"""

from sklearn import datasets, linear_model, preprocessing
reg = linear_model.LogisticRegression(C=1e5)
reg.fit(Xtr, ytr)

print(reg.coef_)
print(reg.intercept_)

yhat = reg.predict(Xts)
acc = np.mean(yhat == yts)
print("Accuracy on test data = %f" % acc)

"""**Instead of taking this approach, we will implement the regression function using gradient descent.**

### Question 2a. Gradient descent for logistic regression [20 pts]
In the class we saw that the weight vector can be found by minimizing the negative log likelihood over $N$ training samples.  The negative log likelihood is called the *loss* function.  For the logistic regression problem, the loss function simplifies to

$$L(\mathbf{w}) = - \sum_{i=1}^N y_i \log \sigma(\mathbf{w}^T\mathbf{x}_i+b) + (1-y_i)\log [1-\sigma(\mathbf{w}^T\mathbf{x}_i+b)].$$

Gradient can be computed as $$\nabla_\mathbf{w}L = \sum_{i=1}^N(\sigma(\mathbf{w}^T\mathbf{x}_i)-y_i)\mathbf{x}_i ,~~~ \nabla_b L = \sum_{i=1}^N(\sigma(\mathbf{w}^T\mathbf{x}_i)-y_i).$$


We can update $\mathbf{w},b$ at every iteration as  
$$ \mathbf{w} \gets \mathbf{w} - \alpha \nabla_\mathbf{w}L, \\ b \gets b - \alpha \nabla_b L.$$ 

**Note that we could also append the constant term in $\mathbf{w}$ and append 1 to every $\mathbf{x}_i$ accordingly, but we kept them separate in the expressions above.**

**Gradient descent function implementation** 

We will use this loss function and gradient to implement a gradient descent-based method for logistic regression.

Recall that training a logistic function means finding a weight vector `w` for the classification rule:

    P(y=1|x,w) = 1/(1+\exp(-z)), z = w[0]+w[1]*x[1] + ... + w[d]x[d]
    
The function implemented should follow the following format:
```python
def logistic_regression_gd(X,y,learning_rate = 0.001,max_iter=1000,tol=pow(10,-5)):
```
Where `X` is the training data feature(s), `y` is the variable to be predicted, `learning_rate` is the learning rate used ($\alpha$ in the slides), `max_iter` defines the maximum number of iterations that gradient descent is allowed to run, and `tol` is defining the tolerance for convergence (which we'll discuss next).

The return values for the above function should be (at the least) 1) `w` which are the regression parameters, 2) `all_cost` which is an array where each position contains the value of the objective function $L(\mathbf{w})$ for a given iteration, 3) `iters` which counts how many iterations did the algorithm need in order to converge to a solution.

Gradient descent is an iterative algorithm; it keeps updating the variables until a convergence criterion is met. In our case, our convergence criterion is whichever of the following two criteria happens first:

- The maximum number of iterations is met
- The relative improvement in the cost is not greater than the tolerance we have specified. For this criterion, you may use the following snippet into your code:
```python
np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol
```
"""

# TODO 
# Your code for logistic regression via gradient descent goes here 

def compute_cost(X,w,y,b):
    # your code for the loss function goes here 
  m = X.shape[0]
  prob = 1/(1+ np.exp(-(X.transpose()*w + b)))
  L = - np.sum(y*np.log(prob) + (1-y)*np.log(1-prob))
  return L

def logistic_regression_gd(X,y,learning_rate = 0.00001,max_iter=1000,tol=pow(10,-5)):
    # your code goes here 
  w = 10  #pick random number
  b = -5  #pick random number
  m = len(y)
  all_cost = np.zeros(max_iter)
  iters = 0;
  for it in range(max_iter):
    # 1/(1+np.exp(-w*xp-b))
    prob = 1/(1+ np.exp(-(X.transpose()*w+b)))
    w = w - learning_rate* np.sum(np.dot((prob-y),X))
    b = b - learning_rate* np.sum(prob-y)
    all_cost[it] = compute_cost(X,w,y,b)
    iters += 1
    if np.absolute(all_cost[it] - all_cost[it-1])/all_cost[it-1] <= tol:
      break
      
  return w, all_cost, iters, b

"""### Question 2b: Convergence plots and test accuracy [10 pts]

After implementing gradient descent for logistic regression, we would like to test that indeed our algorithm converges to a solution. In order see this, we are going to look at the value of the objective/loss function $L(\mathbf{w})$ as a function of the number of iterations, and ideally, what we would like to see is $L(\mathbf{w})$ drops as we run more iterations, and eventually it stabilizes. 

The learning rate plays a big role in how fast our algorithm converges: a larger learning rate means that the algorithm is making faster strides to the solution, whereas a smaller learning rate implies slower steps. In this question we are going to test two different values for the learning rate:
- 0.001
- 0.00001

while keeping the default values for the max number of iterations and the tolerance.


- Plot the two convergence plots (cost vs. iterations)
- Calculate the accuracy of classifier on the test data `Xts` 
- What do you observe?

**Calculate accuracy of your classifier on test data**

To calculate the accuracy of our classifier on the test data, we can create a predict method. 

Implement a function `predict(X,w)` that provides you label 1 if $\mathbf{w}^T\mathbf{x} + b > 0$ and 0 otherwise.
"""

(np.dot(X.transpose(),w) + b) > 0

yhat = ((np.dot(X.transpose(),w) + b) > 0).astype(int)
yhat

# TODO 
# Predict on test samples and measure accuracy
def predict(X,w,b):
  # your code goes here 
  yhat = ((np.dot(X.transpose(),w) + b) > 0).astype(int)
  return yhat

# TODO 
# test gradient descent with step size 0.001
# test gradient descent with step size 0.00001
(w, all_cost,iters, b) = logistic_regression_gd(Xtr,ytr,learning_rate = 0.001,max_iter = 1000, tol=pow(10,-6))  
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss') 

yhat = predict(Xts,w, b)
acc = np.mean(yhat == yts)
print("Test accuracy = %f" % acc)
# complete the rest

(w, all_cost,iters, b) = logistic_regression_gd(Xtr,ytr,learning_rate = 0.00001,max_iter = 1000, tol=pow(10,-6))  
plt.semilogy(all_cost[0:iters])    
plt.grid()
plt.xlabel('Iteration')
plt.ylabel('Training loss') 

yhat = predict(Xts,w, b)
acc = np.mean(yhat == yts)
print("Test accuracy = %f" % acc)

# complete the rest

"""Observations: 

1. Different learning rate affect how fast you reach the lowest training loss. The result indicates the step size for 0.001 is faster than 0.00001.
1.  Compare to the gradient descent for linear regression, gradient descent for logistic regression is much faster to find the decision boundary on the same step size.
"""