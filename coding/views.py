import traceback
from django.shortcuts import render
from coding.models import *
from coding.harness import *


def code(request, difficulty=False, slug=False):
  info = False
  error = False
  if not slug:
    if not difficulty:
      tests = CodingTest.objects.filter(approved=True).order_by(
                                               'difficulty').order_by('name')
    else:
      tests = CodingTest.objects.filter(approved=True, difficulty=difficulty
                                                            ).order_by('name')
    return render(request, 'coding/code.html', {'tests': tests, 'difficulty':
                                                                  difficulty})
  test = CodingTest.objects.get(slug=slug, approved=True,
                                                difficulty=difficulty.title())
  yourcode = test.solution.splitlines()[0]
  results = displayResults(eval(test.tests))
  if request.method == 'POST':
    yourcode = request.POST['code']
    code = validateCode(request.POST['code'])
    if not code:
      error = 'Code did not validate, print statements are not allowed.'
      return render(request, 'coding/code.html', {'error': error, 'info': info,
                          'test': test, 'code': yourcode, 'results': results})
    funcname = getFunctionName(code)
    if not funcname:
      error = 'Function name not found in your code.'
      return render(request, 'coding/code.html', {'error': error, 'info': info,
                          'test': test, 'code': yourcode, 'results': results})
    ns = createNameSpace(code)
    if type(ns) == tuple:
      error = ' '.join(traceback.format_exception(ns[0], ns[1], ns[2])[2:])
      return render(request, 'coding/code.html', {'error': error, 'info': info,
                          'test': test, 'code': yourcode, 'results': results})
    result = testCode(ns, funcname, eval(test.tests))
    if type(result) == tuple:
      error = ' '.join(traceback.format_exception(result[0], result[1],
                                                               result[2])[2:])
      result = eval(test.tests)
  else:
    result = eval(test.tests)
  results = displayResults(result)
  return render(request, 'coding/code.html', {'error': error, 'info': info,
                          'test': test, 'code': yourcode, 'results': results})

def create(request):
  info = False
  error = False
  form = False
  if request.method == 'POST':
    form = request.POST
    newtest = createNewTest(form)
    if newtest[0]:
      info = newtest[1]
    else:
      error = newtest[1]
  return render(request, 'coding/create.html', {'error': error, 'info': info,
                                                                'form': form})
