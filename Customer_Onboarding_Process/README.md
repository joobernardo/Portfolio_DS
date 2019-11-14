**Situation**  

Startup, based on SaaS business model, were growing but not on desired growth. MRR Booking was increasing faster than Active MRR that the Customer Onboarding Department could implement.

The Customer Onboarding Department had 7 operational workers (including me and uses Pipefy (https://www.pipefy.com/) as a management platform. The processes were known but the team often had bottleneck issues in different parts of the process where task forces were needed to be resolved generating inefficiency in the implementation process and sometimes impacting the customer experience.

In Pipefy, each customer is represented by a Card and it goes through 9 parallel processes that are described by Pipes and together they add up to 48 Phases.


**Task**

Create a visualization tool to predict process bottlenecks so that the team can act before it happens and create a 360º view for each customer in order to define the customer onboarding prioritization.


**Action**

I wrote a code in Python to connect to Pipefy (via its API) and manipulate data to plot it directly in Power BI. First, I focused on understanding the Pipefy API and how to write a query in GraphQL in order to get the data I need. After that, I manipulated the data describing how the Customer Onboarding process works and applied a logic rule aiming to identify the bottleneck process. There is also a query in GraphQL to find which phase each customer is in each pipe. Finally, I plotted it on PowerBI.


**Results**

Now the Customer Onboarding Team has a tool where they can identify or predict the process bottleneck. Also the 360º view for each customer allow better planning making the team more efficient.
