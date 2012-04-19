"""
Effectively a slightly less simple "register.simple_tag" decorator.
With the context_tag decorator, it is possible to access the context
in addition to returning a string.

Example:

  from django.template import Library
  register = Library()
       
  @context_tag(register)
  def my_context_tag(context):
    context['my_context_var'] = "whatever"
    return "this will be echoed"


We can even do variables without worrying about unpacking or resolving them:

  @context_tag(register)
  def my_context_tag(context, arg1, arg2):
    # arg1 are regular python objects - already resolved to the context.
    return str(arg1 + arg2)

Note that the tag name is not passed as an argument.
"""

__all__ = ['context_tag']

from django.template import Node, Variable, TemplateSyntaxError
     

class ContextTagNode(Node):
  def __init__(self, f, *args):
    self.f = f

    def make_variable(arg):
      return None if arg == "None" else Variable(arg)

    self.args = map(make_variable, args)

  def render(self, context):
    return self.f(context, *[(a.resolve(context) if a != None else None) for a in self.args])



class context_tag():
  def __init__(self, register, name = None):
    self.register = register
    self.name = name

  def __call__(self, f):
    @self.register.tag(self.name or f.__name__)
    def new(parser, token):
      all_args = token.split_contents()

      # The first argument is the tag name, but we don't care about that.
      template_args = token.split_contents()[1:]

      min_args, max_args = get_arg_range(f)
      min_args -= 1  # The function takes context as its first argument,
      if max_args != None:
        max_args -= 1  # which isn't counted here.

      if not (min_args <= len(template_args) and (len(template_args) <= max_args or max_args == None)):
        import inspect
        function_args = inspect.getargspec(f).args[1:]
        raise TemplateSyntaxError, "%s tag expects arguments: %s" % (all_args[0],
                                                                     ", ".join(function_args))

      return ContextTagNode(f, *template_args)
    return new



def get_arg_range(func):
  """
  Returns (min, max), of the possible numbers of arguments func can take.

  eg:

  >>> def f(a, b, c = 0, d = 1):
  >>>   pass
  >>> get_arg_range(f)
  (2, 4)

  Does not currently handle variable arguments or keyword arguments.
  """
  
  import inspect

  argspec = inspect.getargspec(func)

  args, varargs, varkw, defaults = argspec

  num_default_args = len(defaults) if defaults else 0

  max_args = None if varargs else len(args)
  min_args = len(args) - num_default_args

  return (min_args, max_args)
