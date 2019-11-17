# Junction2019
 A Personalized Shopping Consultant that reduces mispurchases by diagnosing customer’s needs and recommending curated products

## Team SK5
Our solution involves 3 steps: diagnosing customer's needs using computer vision, recommending curated products based on extracted features and a virtual placement of the product on customers.

For demonstration purposes, we are only using cosmetics as a case study.

Diagnosing Customer's Needs:
- Utilizing Haar Cascade feature extractor to segment the skin from the user's facial image
- Analyzing the skin to diagnose severity skin conditions (e.g. Acne)

Recommending Curated Products:
- Match products with the diagnosed skin condition:
- The curated database was developed from K-means clustering based on the ingredients in each of the products with semi-supervised learning.

Virtual Placement of Product on Customer:
- The system generates expected customer's facial image after product usage, using the Neural Style Transfer

The entire stack is developed using Kivy which takes advantage of GPU resources to run the Computer Vision algorithms in with low latency, at 24 frames per second. 
We have separate layers of logic that can afford latency extracted out in a backend, built using Flask as a framework. We integrate the use of both MySQL and MongoDB to deal with the diverse nature of our data. 
Lastly, to deal with the intensive API calls, we make use of Apache Kafka as a FIFO request queue to maximise the scalability of our system as traffic scale up.
