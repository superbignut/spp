+ metaclass

[docs.python.org](https://docs.python.org/3/library/functions.html#type)中有介绍type的两种用法，分别是用来创建类，和查看对象的类型

  + class type(object)
  + class type(name, bases, dict, **kwds)
    
  > With one argument, return the type of an object. The return value is a type object and generally the same object as returned by object.__class__.The isinstance() built-in function is recommended for testing the type of an object, because it takes subclasses into account.

  > With three arguments, return a new type object. This is essentially a dynamic form of the class statement. The name string is the class name and becomes the __name__ attribute. The bases tuple contains the base classes and becomes the __bases__ attribute; if empty, object, the ultimate base of all classes, is added. The dict dictionary contains attribute and method definitions for the class body; it may be copied or wrapped before becoming the __dict__ attribute. The following two statements create identical type objects:

        class X:
            a = 1
        
        X = type('X', (), dict(a=1)) # 相同的作用

[docs.python.org](https://docs.python.org/3/reference/datamodel.html#metaclasses)3.3.3.1节：

> By default, classes are constructed using type(). The class body is executed in a new namespace and the class name is bound locally to the result of type(name, bases, namespace).

+ 这里是说，其实是又创建了一个新的namespace来执行body

> The class creation process can be customized by passing the metaclass keyword argument in the class definition line, or by inheriting from an existing class that included such an argument. In the following example, both MyClass and MySubclass are instances of Meta:

        class Meta(type):
            pass

        class MyClass(metaclass=Meta): # 显示指出元类
            pass

        class MySubclass(MyClass):     # 继承一个显示指出元类的类
            pass
+ 显示的指出元类参数，或者继承一个显示指出元类的类，就可以自定义当前这个类的创建过程

> Any other keyword arguments that are specified in the class definition are passed through to all metaclass operations described below.

> When a class definition is executed, the following steps occur:

  + MRO entries are resolved;

      + 运行时在搜索对象的属性或方法时，需要遵循一定的顺序规则，这个规则称为：Method Resolution Order (MRO).
      + 这里暂时理解为查看是否指定继承

  + the appropriate metaclass is determined;

      + 是否指定元类

  + the class namespace is prepared;
      + 创建新的命名空间
       
  + the class body is executed;
      + 执行body

  + the class object is created.
      + 创建成功
  
[docs.python.org](https://docs.python.org/3/reference/datamodel.html#metaclasses)3.3.3.3节：

The appropriate metaclass for a class definition is determined as follows:

+ if no bases and no explicit metaclass are given, then type() is used;

+ if an explicit metaclass is given and it is not an instance of type(), then it is used directly as the metaclass;

+ if an instance of type() is given as the explicit metaclass, or bases are defined, then the most derived metaclass is used.

+ 第二条是如果不使用一个type的实例作为元类，也就是用其他名字的元类作为metaclass，那么就直接用这个元类
+ 第三条是如果是type的实例作为元类，并且还指定了继承，则找到派生程度最高的类当元类，不太理解

> The most derived metaclass is selected from the explicitly specified metaclass (if any) and the metaclasses (i.e. type(cls)) of all specified base classes. The most derived metaclass is one which is a subtype of all of these candidate metaclasses. 

