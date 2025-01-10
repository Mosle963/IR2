from django.db import models


class Document(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Term(models.Model):
    term = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.term

class TermDocument(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return f'{self.term.term} in {self.document.question}'
