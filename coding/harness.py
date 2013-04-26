import re
import sys
import traceback
from Queue import Queue
from settings import DEBUG
from coding.models import *
from threading import Thread
from google.appengine.api import users
from django.template.defaultfilters import slugify


funcre = re.compile('(?<=^def )\w+')
q = Queue()


def createNewTest(data):
  user = users.get_current_user()
  app = True
  if not user:
    return (False, "You must login.")
  slug = slugify(data['name'])
  try:
    if CodingTest.objects.get(slug=slug):
      return (False, "Test with that name already exists")
  except CodingTest.DoesNotExist:
    pass
  ct = CodingTest(name=data['name'], prompt=data['prompt'], slug=slug,
    difficulty=data['difficulty'], submitter=user, approved=app)
  # Verify tests
  tests = convertTests(data['tests'])
  if type(tests) == str:
    return (False, tests)
  ct.tests = convertTests(data['tests'])
  # Verify solution
  ns = createNameSpace(data['solution'])
  funcname = getFunctionName(data['solution'])
  if not funcname:
    return (False, 'Function name not found in solution.')
  result = testCode(ns, funcname, tests)
  if type(result) == tuple:
    tb = traceback.format_exception(result[0], result[1], result[2])
    return (False, tb)
    #return (False, ''.join(tb[0], tb[2], tb[3]))
  ct.solution = data['solution']
  for k, v in result.iteritems():
    # @@@ Problem here
    if len(v) < 4:
      return (False, "Test failed for %s %s %s" % (k, v[0], v[2]))
  # Save test
  ct.save()
  return (True, "Successfully created test.")

def getFunctionName(code):
  funcname = funcre.search(code)
  if not funcname:
    return False
  return funcname.group(0)

def validateCode(snippet):
  for line in snippet.splitlines():
    line = line.strip()
    if line.startswith('print ') or line.startswith('sys.std'):
      return False
  return snippet

def convertTests(tests):
  t = {}
  for line in tests.splitlines():
    sep = [x for x in ['==', '!='] if x in line]
    if len(sep) != 1:
      return "Tests validation error, invalid operator in '{0}'".format(line)
    line = line.split(sep[0])
    t[unicode(eval(line[0].strip()))] = [sep[0], eval(line[0].strip()), eval(line[1].strip())]
  return t

def createNameSpace(code):
  '''
  Accepts a string which defines a function.  Compiles the function into
  executable Python code and returns a namespace containing the function.
  '''
  ns = {}
  try:
    compile(code, '<string>', 'exec')
    exec code in ns
  except:
    return sys.exc_info()
  return ns

def testCode(ns, func, tests):
  '''
  Accepts a namespace, function name, and test data.  Runs the test data
  through the specified function and returns the results.
  '''
  q.put((ns, func, tests))
  t = Thread(target=testThread())
  t.start()
  t.join(10)
  if t.isAlive():
    t.join()
    return False
  return q.get()

def testThread():
  (ns, func, tests) = q.get()
  try:
    for k, v in tests.iteritems():
      if len(k) == 1:
        if v[0] == '==':
          tests[k].append(ns[func](k[0]) == v[2][0])
        if v[0] == '!=':
          tests[k].append(ns[func](k[0]) != v[2][0])
      elif len(k) == 2:
        if v[0] == '==':
          tests[k].append(ns[func](k[0], k[1]) == v[2][0])
        if v[0] == '!=':
          tests[k].append(ns[func](k[0], k[1]) != v[2][0])
    q.put(tests)
  except:
    q.put(sys.exc_info())

def displayResults(result):
  results = {}
  for k in result:
    if len(result[k]) > 3 and result[k][3]:
      results[('%s %s %s' % (result[k][1], result[k][0], result[k][2]))] = True
    else:
      results[('%s %s %s' % (result[k][1], result[k][0], result[k][2]))] = False
  return results
