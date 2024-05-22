---
{
    "title": "How do we trust Machine Learning algorithms in Medicine?",
    "short_title": "Uncertainty Quantification in Healthcare",
    "pub_date": "2019-09-01",
    "last_mod": "2024-02-05",
    "author": "William van Doorn"
}
---

<p align="center">
  <img src="/01_uncertainty/fig1.png" alt="drawing" width="80%"/> <br>
</p>

# Uncertainty Quantification in Healthcare: Trusting Machine Learning Algorithms

### Introduction 

Recent advancements in machine learning (ML) have paved the way for deploying machine learning-based decision support systems in various sectors, including medicine. Many of these systems have demonstrated superior performance compared to traditional systems or medical specialists. However, despite their potential, most of these systems are not integrated into daily clinical care due to the lack of certain crucial features. One such feature is the **level of trust** that medical specialists can, or should, have in algorithmic predictions. For instance, consider a scenario where an algorithm predicts the day of re-admission to assist a clinical specialist in deciding whether a patient can be discharged. Presently, most machine learning algorithms produce a single "point" prediction (_Figure 1A_), which fails to convey the uncertainty surrounding the prediction. Recent research has introduced "probabilistic" algorithms (_Figure 1B_), which provide a probability distribution, offering a way to quantify uncertainty conveniently.

<p align="center">
  <img src="/01_uncertainty/fig1.png" alt="drawing" width="80%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 1:</b> (A) Point-wise prediction of days to re-admission for patient A (blue) and patient B (orange), without displaying any degree of uncertainty. (B) Probabilistic prediction with uncertainty estimation represented by a probability distribution around the predictions of patients A and B.</span>
</p>

These uncertainty estimates can be invaluable for clinical specialists in contextualizing algorithmic predictions. In this blog post, we'll briefly explore various approaches to modeling predictive uncertainty. Subsequently, we'll delve into a recent implementation based on gradient boosting systems and provide a simple example in an emergency department setting.

### Modeling Predictive Uncertainty

Different approaches to modeling uncertainty using probabilistic algorithms have been outlined in the literature. From a statistical perspective, these methods can be categorized as either non-Bayesian (frequentist) or Bayesian. Additionally, it's preferable to employ algorithms that are either built upon existing architectures or are similar to those that have proven effective for a specific task. In medicine, where structured, tabular data is common, gradient boosting systems have repeatedly demonstrated superiority over other machine learning algorithms [1].

In essence, gradient boosting systems utilize an ensemble of weak learners (such as decision trees), which are iteratively combined to enhance model accuracy. Each tree aims to correct the errors of the preceding stage, leading to sequential improvement in model performance. For a detailed description of gradient boosting in clinical medicine, refer to the attached reference [2]. A recent paper by Tony Duan, Anand Avati, and colleagues introduces the implementation of probabilistic predictions using gradient boosting systems, enabling the quantification of uncertainty [3].

### NGBoost: Natural Gradient Boosting for Probabilistic Prediction

NGBoost is a recently developed gradient boosting algorithm implemented in Python using scikit-learn. Comprehensive source code and implementation details are available on [Github](https://stanfordmlgroup.github.io/projects/ngboost/). NGBoost comprises three essential components: a set of base learners, the probability distribution, and a scoring role (_Figure 2_).

<p align="center">
  <img src="/01_uncertainty/fig2.png" alt="drawing" width="100%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 2:</b> Schematic overview of the NGBoost algorithm, including its three components: base learners, a probability distribution, and a scoring role. Image adapted from the NGBoost <a href="https://stanfordmlgroup.github.io/projects/ngboost/">homepage</a>.</span>
</p>  

While simple decision trees are commonly used as base learners, employing more complex tree structures is also a viable option worth exploring. The choice of probability distribution should align with the output variable; for instance, a Normal distribution is suitable for predicting continuous variables. By modeling a probability distribution over the output, we naturally quantify predictive uncertainties. The quality of these modeled distributions is evaluated by comparing them to the true distribution using a scoring rule. We'll apply this framework to predict days of re-admission in an emergency department setting.

### NGBoost in Practice

The emergency department (ED), with its compressed decision-making timeframe, poses a unique challenge for algorithms assisting clinical specialists. One common decision clinicians face is whether to discharge a patient from the ED safely, considering the risk of re-admission. Hence, our goal is to develop an algorithm that predicts the days to re-admission for individual patients, thereby aiding clinical decision-making.

We have access to a dataset comprising 19,282 patient presentations to an ED, encompassing 11 variables collected during each presentation. These variables include demographic characteristics, medical history, and various laboratory measurements. Additionally, the dataset includes the number of days before a patient was re-admitted to the hospital:  
* Age  
* Sex  
* Time of presentation  
* Days since last admission  
* Clinical risk score (MEDS)   
* Number of comorbidities  
* Number of drugs taken  
* Respiratory rate  
* Hemoglobin level  
* Lactate level    
* CRP level   
* <b>Days to re-admission (outcome)</b>    

Using a standard machine learning workflow, we'll randomly partition this dataset into 70% for algorithm development (the ‘training’ dataset) and reserve the remaining 30% for evaluating our algorithm's performance (the ‘test’ dataset). The corresponding Python code for loading and partitioning our data is as follows:

```python
data = pd.read_csv('/data/emergency_department.csv') # Read data
X_data = data.drop(columns=['readmission_days']) # Extract 11 features for prediction
Y_data = data['readmission_days'] # Extract outcome variable
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30) # Split data into 70% train/30% test
```

We'll initialize our NGBoost algorithm with standard settings: a simple decision tree as the base learner, a Normal distribution for output modeling, and the maximum likelihood estimate (MLE) as our scoring function. Subsequently, we'll train our NGBoost algorithm using data derived from the training dataset.

```python
ngb = NGBRegressor(Base=default_tree_learner, 
              Dist=Normal, 
              Score=MLE(), 
              natural_gradient=True,
              verbose=False)
ngb.fit(X_train, Y_train)
```

After training the NGBoost algorithm, we'll assess its performance on the test dataset, which the algorithm hasn't encountered before. We'll use root mean squared error (RMSE) and negative log-likelihood (NLL) to evaluate overall performance, yielding the following results:

```python
RMSE in test dataset: 3.110
NLL in test dataset: 2.130
```

Overall, the algorithm's performance can be deemed reasonable. However, the true strength of our algorithm lies in individual predictions. Below (_Figure 3_), we present two examples where we visualize the algorithm's prediction, the normal distribution around the prediction, and the true days to re-admission.

<p align="center">
  <img src="/01_uncertainty/fig3.png" alt="drawing" width="100%"/> <br>
  <span style="color:gray; font-size:0.8em;"><b>Figure 3:</b> (A) Example of a prediction and its modeled normal distribution, showing a tightly spaced distribution around the prediction. (B) Example of a prediction and its modeled normal distribution with a wider distribution compared to A, along with a greater distance from the true label than in example A.</span>
</p>  

The modeled distributions around the predictions offer an estimate of the uncertainty associated with each prediction. Notably, the left prediction (_Figure 3A_) exhibits a smaller distribution compared to the right prediction (_Figure 3B_), reflecting the prediction's proximity to the real value.

### Conclusion

Machine learning algorithms have demonstrated impressive discriminatory performance in medicine. However, to be truly effective, they must incorporate features such as uncertainty quantification. In this blog post, we utilized NGBoost, a recent implementation of gradient boosting trees, to provide probabilistic predictions in an emergency department dataset. We successfully predicted days to re-admission for individual patients while offering individual uncertainty measures. These probabilistic predictions represent a significant step towards developing more comprehensive machine learning algorithms for medicine.

**References**  
1. Fernandez-Delgado, M., Cernadas, E., Barro, S., and Amorim, D. Do we need hundreds of classifiers to solve real-world classification problems? The Journal of Machine Learning Research, 15(1):3133–3181, 2014  
2. Zhang, Z., Zhao, Y., Canes, A., Steinberg, D., Lyashevska, O., & , . (2019). Predictive analytics with gradient boosting in clinical medicine. Annals of translational medicine, 7, 152.  
3. Duan, T., Avati, A., Ding, D., Basu, A., Andrew, N.G., & Schuler, A. (2019). NGBoost: Natural Gradient Boosting for Probabilistic Prediction. arXiv e-prints, arXiv:1910.03225.  
