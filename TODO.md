# Analytics Visualizer and Analytics Format
- the current format for analytics is not satisfactory , doesnt support proper multiple lines or plots within same group
- the current analytics format also lack control over the x axis and y axis simultaneously , the format doesnt feel intuitive
- add labels graph type that selects just the first element in array and displays it plainly

# Rule Parser
- focus on getting field names into arrays first
- then run aggregate functions ontop of it
- run element wise multli array functions such as add_arrays
- then run transformation functions on top of the array values
- have combine,filter,sort,map

---

Remember for advanced cross column or cross source stuff the user is supposed to do transformation using comparison engine and chaning the output from that comparison to the next comparison and do those kinda crazy stuff before passing stuff to analytical engine. Its just a data shaper tbh, but with plans to introduce analtyical capability in the future some time

---


# Build Pipeline
1. Integration
2. Format Standardization -> Dummy analytics json body rturn
3. Build Front End Table and Visualizers ( parallel )

ETA : 3PM