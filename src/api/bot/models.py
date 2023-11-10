from django.db import models


class Area(models.Model):
    """
    Area model

    id: int
        Id of area
    area: str
        The area name
    """

    area = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.area

class FAQ(models.Model):
    """
    Question and answer model

    id: int
        Id of QA
    area: int
        The area the question is under
    question: str
        The question
    answer: str
        The answer
    """

    area = models.ForeignKey(Area,on_delete=models.CASCADE, related_name="faq")
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.area} - {self.question} - {self.answer}"

