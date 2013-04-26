from django.db import models


DIFFICULTY_CHOICES = (
  ('EA', 'Easy'),
  ('MO', 'Moderate'),
  ('DI', 'Difficult'),
  ('EX', 'Expert'),
)

class CodingTest(models.Model):
  slug = models.CharField(max_length=500, primary_key=True,
    help_text="Slug for the coding test.")
  name = models.CharField(max_length=500,
    help_text="Name of the coding test.")
  prompt = models.TextField(
    help_text="Prompt to describe the problem to the coder.")
  tests = models.TextField(help_text="Tests to run user's code through.")
  solution = models.TextField(
    help_text="Provide one possible solution that satisfies the tests.")
  difficulty = models.CharField(max_length=2, choices=DIFFICULTY_CHOICES,
    help_text="The difficulty of this problem.")
  submitter = models.CharField(max_length=250,
    help_text="The submitter of this problem.")
  created = models.DateField(auto_now_add=True,
    help_text="Time when server was added.")
  approved = models.BooleanField(default=False,
    help_text="Whether the test has been approved.")
  def __unicode__(self):
    return self.name

