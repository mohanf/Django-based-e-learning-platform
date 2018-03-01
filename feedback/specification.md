Project Specification Feedback
==================

Commit graded: 5ed72cfb6e915d0104a97dd1e92a78962ba56a72

### The product backlog (10/10)

The product backlog looks good overall. Two minor suggestions: 
1. Use a spreadsheet to keep track of the backlog tasks, since it will be easier to update the requirements that way 
2. Include cost estimates (in hours) for each task so that you can track the overall progress

You can also perform a web image search for "product backlog" or "spring backlog" to see what fields teams generally keep in these documents.

### Data models (10/10)

I am understanding it correctly, since Lecture and Test are each a type of Module, it might be better to have Lecture and Test each extend the Module model (instead of using foreign key to link them). A similar thing can be done for Reading and Video, since they are each a type of the Part model and for MCQuestion and BFQuestion, since they are both a type of Question. I am also not completely sure what the UserProgressTotal and UserProgressLecture models are for, and why they need to be separate. It might be helpful to include some comments to make the purpose of each model for clear.

### Wireframes or mock-ups (10/10)

### Additional Information

---
#### Total score (30/30)
---
Graded by: Asra Mahmood (asram@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/Team291/blob/master/feedback/specification-feedback.md