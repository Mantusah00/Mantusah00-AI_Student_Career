# Transparent weighted-interest matching prototype, not a validated career test.
WEIGHTS = {
"Web Developer":[1,1.5,1,.2,.2,.2,0,0,.8,.8,1,.7],
"Data Analyst":[.4,.1,0,1.5,1.5,.8,0,.1,0,.9,.6,1.2],
"AI/ML Engineer":[1.2,.2,.2,1,1.2,1.6,.2,.2,0,1.2,1.3,.8],
"Cybersecurity":[.8,.1,0,.2,.2,.4,1.7,1.5,0,1.3,.7,.5],
"Mobile App Developer":[1,.7,1.7,.2,.1,.2,.1,.2,.7,.8,.8,.7],
"UI/UX Designer":[.2,.8,.6,0,0,0,0,0,1.8,.5,.1,.2]}
def recommend_careers(values):
    results=[]
    for career, weights in WEIGHTS.items():
        raw=sum(v*w for v,w in zip(values,weights))/sum(weights)
        results.append({"career":career,"score":round(max(0,min(100,(raw-1)*25)),1)})
    return sorted(results,key=lambda x:x["score"],reverse=True)[:3]
