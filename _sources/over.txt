オーバーロード(Overloading)
================================================================================

オーバーロード可能な宣言(Overloadable declarations)
--------------------------------------------------------------------------------



シグネチャが異なっていれば、どのような関数、あるいは関数テンプレートでもオーバーロードできるわけではない。以下は、オーバーロードでは考慮されないシグネチャ上の違いである。



* 
  戻り値の型



  .. code-block:: c++  
    
    int f( int ) { return 0 ; }
    double f( int ) { return 0.0 ; } // エラー、オーバーロードできない
  


* 
  メンバー関数とメンバー関数テンプレートにおいて、staticと非staticの違い



  .. code-block:: c++  
    
    struct Foo
    {
        void f() ;
        static void f() ; // エラー
    } ;
  


* 
  
メンバー関数とメンバー関数テンプレートにおいて、リファレンス修飾子の有無が混在している場合



  
メンバー関数の暗黙のオブジェクト仮引数のリファレンスによるオーバーロードを行いたい場合は、lvalueリファレンスでも、リファレンス修飾子を省略することはできない。



  .. code-block:: c++  
    
    struct Foo
    {
        void f() ; // リファレンス修飾子の省略、暗黙にlvalueリファレンス
        void f() && // エラー、他の宣言でリファレンス修飾子が省略されている
    
        void g() & ; // OK
        void g() && ; // OK
    
    } ;
  


* 
  仮引数の型が、同じ型を指す異なるtypedef名の場合



  .. code-block:: c++  
    
    using Int = int ;
    
    void f( int ) ;
    void f( Int ) ; // 再宣言
  

  
typedef名は単なる別名であって、異なる型ではないので、シグネチャはおなじになる。




* 
  
仮引数の型の違いが、*か[]である場合



  
<a href="#dcl.fct">関数の型</a>で説明したように、仮引数のポインターと配列のシグネチャは同じである。ただし、2つ目以降の配列は考慮されるので注意。



  .. code-block:: c++  
    
    void f( int * ) ;
    void f( int [] ) ; // 再宣言、void f(int *)と同じ
    void f( int [2] ) ; // 再宣言、void f(int *)と同じ
    
    void f( int [][2] ) ; // オーバーロード、シグネチャはvoid f(int(*)[2])
  


* 
  
仮引数が関数型か、同じ関数型へのポインターである場合



  
<a href="#dcl.fct">関数の型</a>で説明したように、仮引数としての関数型は同じ関数型へのポインター型に変換される。



  .. code-block:: c++  
    
    void f( void(*)() ) ;
    void f( void () ) ; // 再宣言
    void f( void g() ) ; // 再宣言
  

  
これらはオーバーロードではない。




* 
  
仮引数のトップレベルのCV修飾子の有無



  
<a href="#dcl.fct">関数の型</a>で説明したように、仮引数のトップレベルのCV修飾子は無視される。トップレベル以外のCV修飾子は別の型とみなされるので、オーバーロードとなる。



  .. code-block:: c++  
    
    void f( int * ) ;
    void f( int * const ) ; // 再宣言
    void f( int * volatile ) ; // 再宣言
    void f( int * const volatile ) ; // 再宣言
    
    void f( int const * ) ; // オーバーロード
    void f( int volatile * ) ; // オーバーロード
    void f( int const volatile * ) ; // オーバーロード
  




.. code-block:: c++
  
  void f( int, int ) ;
  void f( int, int = 0 ) ; // 再宣言
  void f( int = 0, int ) ; // 再宣言


オーバーロードのその他の注意事項
--------------------------------------------------------------------------------



オーバーロード解決は、名前解決によって複数の宣言が列挙される場合に行われる。内側のスコープによって名前が隠されている場合は、オーバーロード解決は行われない。



たとえば、派生クラスで基本クラスのメンバー関数名と同名のものがある場合、そのメンバー関数は基本クラスのメンバー関数の名前を隠す。



.. code-block:: c++
  
  struct Base
  {
     void f( int ) { }
  } ;
  
  struct Derived : Base
  {
      void f( double ) { } // Base::f(int)を隠す
  } ;
  
  
  int main()
  {
      Derived d ;
      d.f( 0 ) ; // Derived::f(double)が呼ばれる
  }


似たような例に、関数のローカル宣言がある。



.. code-block:: c++
  
  void f( int ) { }
  void f( double ) { }
  
  int main()
  {
      f( 0 ) ; // f(int)を呼び出す
      void f( double ) ; // f(int)を隠す
      f( 0 ) ; // f(double)を呼び出す
  }


オーバーロードされたメンバー関数は、それぞれ別々のアクセス指定を持つことができる。アクセス指定は名前解決には影響しないので、オーバーロード解決は行われる。



.. code-block:: c++
  
  class X
  {
  private :
      void f( int ) { }
  public :
      void f( double ) { }
  
  } ;
  
  int main()
  {
      X x ;
      x.f( 0 ) ; // エラー、X::f(int)はprivateメンバー
  }


この例では、オーバーロード解決によって、X::f(int)が選ばれるが、これはprivateメンバーなので、Xのfriendではないmain関数からは呼び出せない。よってエラーになる。



オーバーロード解決(Overload resolution)
--------------------------------------------------------------------------------



オーバーロードされた関数を呼び出す際に、実引数から判断して、最もふさわしい関数が選ばれる。これを、オーバーロード解決(Overload resolution)と呼ぶ。オーバーロード解決のルールは非常に複雑である。単純に実引数と仮引数の型が一致するだけならまだ話は簡単だ。



.. code-block:: c++
  
  void f( int ) { }
  void f( double ) { }
  
  int main()
  {
      f( 0 ) ; // f(int)が呼ばれる
      f( 0.0 ) ; // f(double)が呼ばれる
  }


この結果には、疑問はない。実引数と仮引数の型が一致しているからだ。しかし、もし、実引数の型と仮引数の型が一致していないが、暗黙の型変換によって仮引数の型に変換可能な場合、問題は非常にややこしくなる。



.. code-block:: c++
  
  void f( int ) { }
  void f( double ) { }
  
  int main()
  {
      short a = 0 ;
      f( a ) ; // f(int)を呼ぶ
  
      float b = 0.0f ;
      f( b ) ; // f(double)を呼ぶ
  }


この結果も、妥当なものである。shortは整数型なので、doubleよりはintを優先して欲しい。floatは、浮動小数点数型なので、doubleを優先して欲しい。



では、以下のような場合はどうだろうか。



.. code-block:: c++
  
  void f( int ) { }
  void f( long long ) { }
  int main()
  {
      long a = 0l ;
      f( a ) ; // 曖昧
  
      short b = 0 ;
      f( b ) ; // f(int)を呼び出す
  }


この結果は、少し意外だ。比べるべき型は、intとlong long intである。long型を渡すと曖昧になる。しかし、short型を渡すと、なんとint型が選ばれる。こちらは曖昧にならない。これは、short型からint型への型変換に<a href="#conv.prom">整数のプロモーション</a>が使われているためである。




では、ユーザー定義の型変換が関係する場合はどうだろうか。



.. code-block:: c++
  
  void f( int ) { }
  
  class X
  {
  public :
      X() = default ;
      X( double ) { } // ユーザー定義の型変換
  } ;
  
  void f( X ) { }
  
  int main()
  {
      f( 0.0 ) ; // f(int)を呼ぶ
  }


この場合、ユーザー定義の型変換より、言語側に組み込まれた、標準型変換を優先している。



では、引数が複数ある場合はどうなるのか。関数テンプレートの場合はどうなるのか。疑問は尽きない。オーバーロード解決のルールは非常に複雑である。これは、できるだけオーバーロード解決の挙動を、人間にとって自然にし、詳細を知らなくても問題がないように設計した結果である。その代償として、オーバーロード解決の詳細は非常に複雑になり、実装にも手間がかかるようになった。



オーバーロード解決の手順を、簡潔にまとめると、以下のようになる。



0 名前探索によって見つかる同名の関数をすべて、候補関数(Candidate functions)として列挙する
1 候補関数から、実際に呼び出すことが可能な関数を、適切関数(Viable functions)に絞る
2 実引数から仮引数への暗黙の型変換を考慮して、最適な関数(Best viable function)を決定する


例えば、以下のようなオーバーロード解決の場合、



.. code-block:: c++
  
  void f() { }
  void f( int ) { }
  void f( int, int ) { }
  void f( double ) { }
  
  void g( int ) { }
  
  int main()
  {
      f( 0 ) ; // オーバーロード解決が必要
  }


候補関数には、f(), f(int), f(int,int), f(double)が列挙される。適切関数には、f(int), f(double)が選ばれる。これを比較すると、f(int)が型一致で最適関数となる。



本書におけるオーバーロード解決の解説は、細部をかなり省略している。



候補関数(Candidate functions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



候補関数(Candidate functions)は、正確に言えば、候補関数群とでも訳されるべきであろう。候補関数とは、その名前の通り、オーバーロード解決の際に呼び出しの優先順位を考慮される関数のことである。候補関数に選ばれなければ、呼び出されることはない。ある名前に対してオーバーロード解決が必要な場合に、まず最初に行われるのが、候補関数の列挙である。候補関数は、通常通りに名前探索をおこなって見つけた関数すべてである。これには、実際には呼び出すことのできない関数も含む。オーバーロード解決の際に考慮するのは、この候補関数だけである。その他の関数は考慮しない。



.. code-block:: c++
  
  void f() { }
  void f( int ) { }
  void g() { }
  
  int main()
  {
      f( 0 ) ; // 候補関数の列挙が必要
  }


ここでの候補関数とは、f()とf(int)である。f()は、実際に呼び出すことができないが、候補関数として列挙される。この場合、g()は候補関数ではない。



オーバーロード解決の際に使われる名前探索は、通常の名前探索と何ら変わりないということに注意しなければならない。例えば、名前が隠されている場合は、発見されない。



.. code-block:: c++
  
  void f( int ) { }
  void f( double ) { }
  
  int main()
  {
      f( 0 ) ; // #1 f(int)
      void f( double ) ; // 再宣言、f(int)を隠す
      f( 0 ) ; // #2 f(double)
  }


#1では、f(int)が名前探索で見つかるので、オーバーロード解決によって、f(int)が最適関数に選ばれる。#2では、f(int)は隠されているので、名前探索では見つからない。そのため、f(int)は候補関数にはならない。結果として、f(double)が最適関数に選ばれる。



関数のローカル宣言はまず使われないが、派生クラスのメンバー関数の宣言によって、基本クラスのメンバー関数が隠されることはよくある。



.. code-block:: c++
  
  struct Base
  {
      void f( int ) { }
      void f( long ) { }
  } ;
  
  struct Derived : Base
  {
      void f( double ) { } // Baseクラスの名前fを隠す
      void g()
      {
          f( 0 ) ; // Derived::f(double)
      }
  } ;


この例では、Derived::f(double)が、Baseのメンバー関数fを隠してしまうので、候補関数にはDerived::f(double)しか列挙されない。





候補関数がメンバー関数である場合、コード上には現れない仮引数として、クラスのオブジェクトを取る。これを、暗黙のオブジェクト仮引数(implicit object parameter)と呼ぶ。これは、オーバーロード解決の際に考慮される。暗黙のオブジェクト仮引数は、オーバーロード解決においては、関数の第一引数だとみなされる。暗黙のオブジェクト仮引数の型は、まず、クラスの型XにCV修飾子がつき、さらに、




リファレンス修飾子がない場合、あるいは、リファレンス修飾子が&amp;の場合、X（場合によってCV修飾子）へのlvalueリファレンス。



.. code-block:: c++
  
  struct X
  {
      // コメントは暗黙のオブジェクト仮引数の型
      void f() & // X &
      void f() const & // X const &
      void f() volatile & // X volatile &
      void f() const volatile & // X const volatile &
  
      viod g() ; // X &
  } ;


リファレンス修飾子が&amp;&amp;の場合、X(場合によってCV修飾子)へのrvalueリファレンス。



.. code-block:: c++
  
  struct X
  {
      // コメントは暗黙のオブジェクト仮引数の型
      void f() && // X &&
      void f() const && // X const &&
      void f() volatile && // X volatile &&
      void f() const volatile && // X const volatile &&
  } ;


となる。例えば、以下のようにオーバーロード解決に影響する。



.. code-block:: c++
  
  struct X
  {
      void f() & ; // #1 暗黙のオブジェクト仮引数の型は、X &
      void f() const & ; // #2 暗黙のオブジェクト仮引数の型は、X const &
      void f() && ; // #3 暗黙のオブジェクト仮引数の型は、X &&
  } ;
  
  int main()
  {
      X x ;
      x.f() ; // #1
      X const cx ;
      cx.f() ; // #2
      static_cast<X &&>(x).f() ; // #3
  } 







候補関数には、メンバー関数と非メンバー関数の両方を含むことがある。



.. code-block:: c++
  
  struct X
  {
      X operator + ( int ) const
      { return X() ; }
  } ;
  
  X operator + ( X const &, double )
  { return X() ; }
  
  int main()
  {
      X x ;
      x + 0 ; // X::operator+(int)
      x + 0.0 ; // operator+(X const &, double)
  }


この場合、候補関数には、メンバー関数であるX::operator +と、非メンバー関数であるoperator+の両方が含まれる。候補関数に列挙されるので、当然、オーバーロード解決で最適関数が決定される。



テンプレートの実引数推定は、名前解決の際に行われる。そのため、候補関数として関数テンプレートのインスタンスが列挙された時点で、テンプレート実引数は決定されている。



オーバーロード解決が行われる文脈には、いくつか種類がある。それによって、候補関数の選び方も違ってくる。




関数呼び出しの文法(Function call syntax)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



最も分かりやすい関数呼び出しは、関数呼び出しの文法によるものだろう。しかし、一口に関数呼び出しの文法といっても、微妙に違いがある。単なる関数名に対する関数呼び出し式の適用もあれば、暮らすのオブジェクトに.や-&gt;を使った式に対する関数呼び出し、つまりメンバー関数の呼び出しや、クラスのオブジェクトに対する関数呼び出し式、つまりoperator ()のオーバーロードを呼び出すものがある。



.. code-block:: c++
  
  struct X
  {
      void f( int ) { }
      void f( double ) { }
  
      void operator () ( int ) { }
      void operator () ( double ) { }
  } ;
  
  int main()
  {
      X x ;
      x.f( 0 ) ; // オーバーロード解決が必要
      x( 0 ) ; // オーバーロード解決が必要
  }


オーバーロード解決は、関数へのポインターやリファレンスを経由した間接的な呼び出しの際には、行われない。



.. code-block:: c++
  
  void f( int ) { }
  void f( double ) { }
  
  int main()
  {
      void (* p)( int ) = &f ;
      p( 0.0 ) ; // f(int)
  }




式中の演算子(Operators in expressions)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



この項は、オーバーロードされた演算子を候補関数として見つける際の詳細である。演算子のオーバーロードの宣言方法については、<a href="#over.oper">オーバーロードされた演算子</a>を参照。



演算子を使った場合にも、オーバーロード解決が必要になる。ただし、演算子にオーバーロード解決が行われる場合、オペランドにクラスやenumが関わっていなければならない。オペランドが基本型だけであれば、組み込みの演算子が使われる。



.. code-block:: c++
  
  // エラー、オペランドがすべて基本型
  int operator + (int, int) { return 0 ; }


演算子のオーバーロードは、メンバー関数としてオーバーロードする方法と、非メンバー関数としてオーバーロードする方法がある。すでに述べたように、候補関数には、どちらも列挙される。



演算子のオーバーロード関数は、演算子を仮に@と置くと、以下の表のように呼ばれる。



====================          ====================          ====================          ====================
種類                    式                    メンバー関数として呼び出す場合                    非メンバー関数として呼び出す場合
====================          ====================          ====================          ====================
単項前置                    @a                    (a).operator@ ( )                    operator@ (a)
単項後置                    a@                    (a).operator@ (0)                    operator@ (a, 0)
二項                    a@b                    (a).operator@ (b)                    operator@ (a, b)
代入                    a=b                    (a).operator= (b)
添字                    a[b]                    (a).operator[](b)
クラスメンバーアクセス                    a->                    (a).operator-> ( )
====================          ====================          ====================          ====================


代入、添字、クラスメンバーアクセスの演算子は、メンバー関数として宣言しなければならないので、非メンバー関数は存在しない。






コンストラクターによる初期化(Initialization by constructor)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



クラスのオブジェクトの直接初期化の場合、そのクラスからコンストラクターが候補関数として列挙され、オーバーロード解決が行われる。



.. code-block:: c++
  
  struct X
  {
      X( int ) { }
      X( double ) { }
  } ;
  
  int main()
  {
      X a( 0 ) ; // オーバーロード解決が行われる
      X b( 0.0 ) ; // オーバーロード解決が行われる
  }




ユーザー定義型変換によるクラスのコピー初期化(Copy-initialization of class by user-defined conversion)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



クラスのコピー初期化におけるユーザー定義型変換には、オーバーロード解決が行われる。ユーザー定義型変換には、変換コンストラクターと変換関数がある。これは、両方とも、候補関数として列挙される。



.. code-block:: c++
  
  struct Destination ;
  extern Destination obj ;
  
  struct Source
  {
      operator Destination &() { return obj ; }
  } ;
  
  
  struct Destination
  {
      Destination() { }
      Destination( Source const & ) { }
  } ;
  
  Destination obj ;
  
  
  int main()
  {
      Source s ;
      Destination d ;
      d = s ; // オーバーロード解決、Source::operator Destination &()
      Source cs ;
      d = cs ; // オーバーロード解決、Destination::Destination( Source const & ) 
  }


この例では、変換コンストラクターと変換関数の両方が候補関数として列挙される。この例で、もし変換コンストラクターの仮引数が、Source &amp;ならば、オーバーロード解決は曖昧になる。



ただし、explicit変換コンストラクターとexplicit変換関数は、直接初期化か、明示的なキャストが使われた際にしか候補関数にならない。



.. code-block:: c++
  
  struct X
  {
      X() { }
      explicit X( int ) { }
      explicit operator int() { return 0 ; }
      
  } ;
  
  int main()
  {
      X x ;
      int a( x ) ; // OK
      int b = x ; // エラー
  
      X c( 0 ) ; // OK
      X d = 0 ; // エラー
  }


この場合の実引数リストには、初期化式が使われる。変換コンストラクターの場合は、第一仮引数と比較され、変換関数の場合は、クラスの隠しオブジェクト仮引数と比較される。




.. code-block:: c++
  
  // 変換コンストラクターの例
  struct A { } ;
  
  struct X
  {
      // 候補関数
      X( A & ) { }
      X( A const & ) { }
  } ;
  
  int main()
  {
      A a ;
      X x1 = a ; // オーバーロード解決、A::A(A&)
      A const ca ;
      X x2 = ca ; // オーバーロード解決、A::A(A const &)
  }


この例では、実引数としてaやcaが使われ、クラスXの変換コンストラクターの第一仮引数と比較される。



.. code-block:: c++
  
  // 変換関数の例
  struct A { } ;
  
  struct X
  {
      // 候補関数
      operator A() & { return A() ; }
      operator A() const & { return A() ; }
      operator A() && { return A() ; }
  
  } ;
  
  int main()
  {   
      X x ;
  // オーバーロード解決、X::operator A() &
  // 実引数はlvalueのX、
      A a1 = x ; 
      X const cx ;
  // オーバーロード解決、X::operator A() const &
  // 実引数はconstなlvalue
      A a2 = cx ; 
  // オーバーロード解決、X::operator A() &&
  // 実引数はxvalue
      A a3 = static_cast<X &&>(x) ; 
  }


この例では、クラスXのオブジェクトが実引数として、変換関数のクラスの隠しオブジェクト仮引数として比較される。たとえば、A a1 = x ; の場合、実引数は非constなlvalueなので、オーバーロード解決により、X::operator A() &amp;が選ばれる。



その他の変換コンストラクターと変換関数に対しても、オーバーロード解決で比較する実引数と仮引数はこれに同じ。





変換関数によるクラスではないオブジェクトの初期化(Initialization by conversion function)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



クラスではないオブジェクトを、クラスのオブジェクトの初期化式で初期化する際、クラスの変換関数が候補関数として列挙され、オーバーロード解決が行われる。実引数リストには、初期化式がひとつの実引数として渡される



.. code-block:: c++
  
  struct X
  {
      operator int() { return 0 ; }
      operator long() { return 0L ; }
      operator double() { return 0.0 ; }
  } ;
  
  int main()
  {
      X x ;
      int i = x ; // オーバーロード解決が行われる
  }


この例では、候補関数に、X::operator int、X::operator long、X::operator doubleが列挙され、オーバーロード解決によってX::operator intが選ばれる。




変換関数によるリファレンスの初期化(Initialization by conversion function for direct reference binding)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



リファレンスを初期化するとき、初期化式に変換関数を適用して、その結果を束縛できる。このとき、クラスの変換関数が候補関数として列挙され、オーバーロード解決が行われる。



.. code-block:: c++
  
  struct X
  {
      operator int() { return 0 ; }
      operator short() { return 0 ; }
  } ;
  
  int main()
  {   
      X x ;
      int && ref = x ; // オーバーロード解決、X::operator int()
  }




リスト初期化による初期化(Initialization by list-initialization)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



<a href="#dcl.init.aggr">アグリゲート</a>ではないクラスがリスト初期化によって初期化されるとき、オーバーロード解決によってコンストラクターが選択される。



この際の候補関数の列挙は、二段階に分かれている。



まず一段階に、クラスの初期化リストコンストラクターが候補関数として列挙され、オーバーロード解決が行われる。実引数リストには、初期化リストが唯一の実引数として、std::initializer_list&lt;T&gt;の形で、与えられる



.. code-block:: c++
  
  struct X
  {
      // 初期化リストコンストラクター
      X( std::initializer_list<int> ) { }
      X( std::initializer_list<double> ) { }
  
      // その他のコンストラクター
      X( int, int, int ) { }
      X( double, double, double ) { }
  } ;
  
  int main()
  {   
      X a = { 1, 2, 3 } ; // オーバーロード解決、X::X( std::initializer_list<int> )
      X b = { 1.0, 2.0, 3.0 } ; // オーバーロード解決、X::X( std::initializer_list<double> )
  }


この場合、候補関数には、初期化リストコンストラクターしか列挙されない。



もし、一段階目の名前解決で、<a href="#over.match.viable">適切</a>な初期化リストコンストラクターが見つからなかった場合、二段階の候補関数として、再びオーバーロード解決が行われる。今度は、クラスのすべてのコンストラクターが候補関数として列挙される。実引数は、初期化リストの中の要素が、それぞれ別の実引数として渡される



.. code-block:: c++
  
  struct X
  {
      // 適切な初期化リストコンストラクターなし
  
      X( int, int, int ) { }
      X( double, double, double ) { }
      X( int, double, int ) { }
  } ;
  
  int main()
  {   
      X a = { 1, 2, 3 } ; // オーバーロード解決、X::X( int, int, int )
      X b = { 1.0, 2.0, 3.0 } ; // オーバーロード解決、X::X( double, double, double )
      X c = { 1, 2.0, 3 } ; // オーバーロード解決、X::X( int, double, int )
  }


「適切」という用語に注意すること。もし、<a href="#dcl.init.list">縮小変換</a>が必要となれば、適切関数かどうかを判定する前にエラーとなる。



.. code-block:: c++
  
  struct X
  {
      X( std::initializer_list<int> ) { }
      X( double, double, double ) { }
  } ;
  
  int main()
  {   
      X b = { 1.0, 2.0, 3.0 } ; // エラー、縮小変換が必要
  }


デフォルトコンストラクターを持つクラスに空の初期化リストが渡された場合、一段階目のオーバーロード解決は行われず、デフォルトコンストラクターが呼ばれる。



.. code-block:: c++
  
  struct X
  {
      X ( ) { }
      template < typename T >
      X( std::initializer_list<T> ) { }
  } ;
  
  int main()
  {   
      X x = { } ; // デフォルトコンストラクターが呼ばれる
  }




コピーリスト初期化では、explicitコンストラクターが選ばれた場合、エラーとなる。



.. code-block:: c++
  
  struct X
  {
      explicit X( int ) { }
  } ;
  
  int main()
  {   
      X a = { 0 } ; // エラー、コピーリスト初期化でexplicitコンストラクター
      X b{ 0 } ; // OK、直接初期化
  }




適切関数(Viable functions)
--------------------------------------------------------------------------------



候補関数は、単に名前探索の結果であり、実際には呼び出すことができない関数も含まれている。このため、候補関数を列挙した後、呼び出すことが出来る関数、すなわち適切関数(Viable functions)を列挙する。



適切関数とは、与えられた実引数で、実際に呼び出すことが出来る関数である。これには、大きく二つの要素がある。仮引数の数と型である。



適切関数となるためにはまず、与えられた実引数の個数に対して、仮引数の個数が対応していなければならない。そのための条件は、以下のいずれかを満たしていればよい。



* 
  
実引数の個数と、候補関数の仮引数の個数が一致する関数



  
これは簡単だ。実引数と同じ個数だけの仮引数があればよい。可変長テンプレートのインスタンス化による関数もこのうちに入る。



  .. code-block:: c++  
    
    void f( int, int ) { }
    
    int main()
    {
        f( 0, 0 ) ; // OK
        f( 0 ) ; // エラー
    }
  


* 
  
候補関数の仮引数の個数が、実引数の個数より少ないが、仮引数リストにエリプシス(...)がある場合。



  
これは、C言語でお馴染みの...のことだ。可変長テンプレートは、このうちには入らない。



  .. code-block:: c++  
    
    void f( int, ... ) ;
    
    int main()
    {   
        f( 0 ) ; // 適切関数
        f( 0, 1 ) ; // 適切関数
        f( 0, 1, 2, 3, 4, 5 ) ; // 適切関数
    }
  


* 
  
候補関数の仮引数の個数は、実引数より多いが、実引数より多い仮引数にはすべて、デフォルト実引数が指定されていること。



  .. code-block:: c++  
    
    void f( int, int = 0, int = 0, int = 0, int = 0, int = 0 ) ;
    
    int main()
    {   
        f( 0 ) ; // 関数
        f( 0, 1 ) ; // 適切関数
        f( 0, 1, 2, 3, 4, 5 ) ; // 適切関数
    }
  




さらに、対応する実引数から仮引数に対して、後述する暗黙の型変換により、妥当な変換が存在しなければならない。



.. code-block:: c++
  
  void f( int ) { }
  
  int main()
  {
      f( 0 ) ; // OK、完全一致
      f( 0L ) ; // OK、整数変換
      f( 0.0 ) ; // OK、整数と浮動小数点数間の変換
      f( &f ) ; // エラー
  }


適切関数であるからといって、実際に呼び出せるとは限らない。たとえば、宣言されているが未定義であったり、アクセス指定による制限を受けたり、あるいはその他実装依存の理由など、現実には呼び出すことができない理由は多数存在する。



最適関数(Best viable function)
--------------------------------------------------------------------------------



適切関数が複数ある場合、定められた方法で関数を比較することによって、ひとつの最も適切(best viable)な関数を選択する。この関数を最適関数と呼ぶ。オーバーロード解決の結果は、この最適関数となる。もし、最も適切な関数をひとつに決定できない場合、オーバーロード解決は曖昧であり、エラーとなる。



最適関数の決定は、主に、後述する暗黙の型変換の優先順位によって決定される。



まず大前提として、ある関数が、別の関数よりも、より適切であると判断されるには、ある関数のすべて仮引数に対する実引数からの暗黙の型変換の優先順位が劣っておらず、かつ、ひとつ以上の優れている型変換が存在しなければならない。



.. code-block:: c++
  
  void f( int, double ) { } // #1
  void f( long, int ) { } // #2
  
  int main()
  {   
      f( 0 , 0 ) ; // エラー、オーバーロード解決が曖昧
  }


この例では、どの関数も、仮引数への型変換の優先順位が、他の関数より劣っている。したがってオーバーロード解決は曖昧となる。一見すると、#2の方が、どちらも整数型であるので、よりよい候補なのではないかと思うかもしれない。しかし、#1の第一仮引数の型はintなので、longよりも優れている。一方、第二引数では、#2の方が優れている。このため、曖昧となる。最適関数となるためには、全ての仮引数の型が、他の候補より劣っていてはならないのだ。



ユーザー定義型変換による初期化の場合、ユーザー定義型変換の結果の型から、目的の型へ、標準型変換により変換する際、より優先順位の高いものが選ばれる。



.. code-block:: c++
  
  struct X
  {
      operator int() ;
      operator double() ;
  
  } ;
  
  void f()
  {   
      X x ;
      int i = x ; // operator intが最適関数
      float f = x ; // エラー、曖昧
  }


一見すると、doubleからfloatへの変換は、intからの変換より優先順位が高いのではないかと思うかもしれないが、後述する標準型変換の優先順位のルールにより、同じ優先順位なので、曖昧となる。



非テンプレート関数と関数テンプレートの特殊化では、非テンプレート関数の特殊化が優先される。



.. code-block:: c++
  
  template < typename T >
  void f( T ) ;
  void f( int ) ;
  
  int main()
  {   
      f( 0 ) ; // 非テンプレート関数を優先
  }


もちろん、これは大前提の、すべての仮引数に対し劣った型変換がないということが成り立つ上での話である。



.. code-block:: c++
  
  template < typename T >
  void f( T ) ;
  void f( long ) ;
  
  int main()
  {   
      f( 0 ) ; // 関数テンプレートの特殊化f<int>を優先
  }


この場合は、テンプレートの特殊化である仮引数int型の方が、実引数int型に対して、より優れた型変換なので、優先される。



テンプレートの実引数推定のルールは複雑なので、一見して、非テンプレート関数が優先されると思われるコードで、関数テンプレートの実体化の方が優先される場合がある。



.. code-block:: c++
  
  // #1
  // 非テンプレート関数
  void f( int const & ) ;
  
  
  // #2
  // 関数テンプレート
  template < typename T >
  void f( T && ) ; 
  
  int main()
  {
      int x = 0 ; // xは非constなlvalue
      f( x ) ; // #2を呼ぶ
  }


これは、#2の実体化の結果が、f&lt;int &amp;&gt;( int &amp; )になるからだ。xは非constなlvalueであるので、非constなlvalueリファレンス型の仮引数と取る#2の方が優先される。



ふたつの関数が両方ともテンプレートの特殊化の場合、<a href="#temp.func.order">半順序</a>によって、より特殊化されていると判断される方が、優先される。



.. code-block:: c++
  
  template < typename T > void f( T ) ; // #1
  template < typename T > void f( T * ) ; // #2
  
  int main()
  {   
      int * ptr = nullptr ;
      f( ptr ) ; // 半順序により#2を優先
  }


#1と#2の特殊化による仮引数の型は、どちらも int *であるが、#2のテンプレートの特殊化の方が、半順序のルールによって、より特殊化されているとみなされるため、#2が優先される。



暗黙の型変換の順序(Implicit conversion sequences)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



暗黙の型変換には、いくつかの種類と、多数の例外ルールがあり、それぞれ優先順位を比較することができる。残念ながら、この詳細は非常に冗長であり、本書では概略の説明に留める。



まず、暗黙の型変換には、大別して三種類ある。<a href="#conv">標準型変換</a>、<a href="#class.conv">ユーザー定義型変換</a>、エリプシス変換である。優先順位もこの並びである。標準型変換が一番優先され、次にユーザー定義型変換、最後にエリプシス変換となる。



.. code-block:: c++
  
  struct X { X(int) ; } ;
  
  void f( int ) ; // #1 
  void f( X ) ; // #2
  
  void g( X ) ; // #3
  void g( ... ) ; // #4
  
  
  int main()
  {
      f( 0 ) ; // #1、標準型変換がユーザー定義型変換に優先される
      g( 0 ) ; // #3、ユーザー定義型変換がエリプシス変換に優先される
  }


さらに、標準型変換とユーザー定義変換同士の間での優先順位がある。



エリプシスに基本型以外を渡して呼び出した場合の挙動は未定義だが、オーバーロード解決には影響しない。



標準型変換（Standard conversion sequences）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



オーバーロード解決における標準型変換の間の優先順位は、非常に複雑で、単に、ランクA＞ランクBのような単純な比較ができない。ここでは、とくに問題になりそうな部分のみ取り上げる。



まず、型変換の必要のない、完全一致が最も優先される。



.. code-block:: c++
  
  void f( int ) ;
  void f( double ) ;
  
  int main()
  {
      f( 0 ) ; // f(int)
      f( 0.0 ) ; // f(double)
  }


この完全一致には、<a href="#conv.lval">lvalueからrvalueへの型変換</a>、<a href="#conv.array">配列からポインターへの型変換</a>、<a href="#conv.func">関数からポインターへの型変換</a>が含まれる。



void f( int ) ;

int main()
{
    int x = 0 ;
    f( x ) ; // lvalueからrvalueへの変換
}



配列や関数からポインターへの変換は、完全一致とみなされることに注意。



.. code-block:: c++
  
  void g( ) ;
  
  void f( void (*)() ) ; // ポインター
  void f( void (&)() ) ; // リファレンス
  
  int main()
  {
      f( g ) ; // エラー、オーバーロード解決が曖昧、候補関数はすべて完全一致
      f( &g ) ; // OK、f( void (*)() )
  }


完全一致は、ポインターやリファレンスに<a href="#conv.qual">CV修飾子を付け加える型変換</a>より優先される。



.. code-block:: c++
  
  void f( int & ) ; // #1
  void f( int const & ) ; // #2
  
  int main()
  {
      int x = 0 ;
      f( x ) ; // #1、完全一致
  }


整数と浮動小数点数のプロモーションは、その他の整数と浮動小数点数への変換より優先される。



.. code-block:: c++
  
  void f( int ) ;
  void f( long ) ;
  
  int main()
  {
      short x = 0 ;
      f( x ) ; // f(int)、プロモーション
  }






オーバーロード関数のアドレス(Address of overloaded function)
--------------------------------------------------------------------------------



ある関数の名前に対して、複数の候補関数がある場合でも、名前から関数のアドレスを取得できる。どの候補関数を選ぶかは、文脈が期待する型の完全一致で決定される。初期化や代入、関数呼び出しの実引数や明示的なキャストの他に、関数の戻り値も、文脈により決定される。



.. code-block:: c++
  
  void f( int ) ;
  void f( long ) ;
  
  void g( void (*)(int) ) ;
  
  void h()
  {
      // 初期化
      void (*p)(int) = &f ; // void f(int)のアドレス
      // 代入
      p = &f ; // void f(int)のアドレス
      // 関数呼び出しの実引数
      g( &f ) ;
      // 明示的なキャスト
      static_cast<void (*)(int)>(&f) ; // void f(int)のアドレス
  }
  
  // 関数の戻り値
  auto i() -> void (*)(int)
  {
      return &f ; // void f(int)のアドレス
  }


これらの文脈では、ある具体的な完全一致の型を期待しているので、オーバーロードされた関数名から、適切な関数を決定できる。



完全一致の型ではない場合や、型を決定できない場合はエラーである。



.. code-block:: c++
  
  void f( int ) ;
  void f( long ) ;
  
  template < typename T >
  void g( T ) { }
  
  int main()
  {
      g( &f ) ; // エラー
  }


オーバーロード演算子(Overloaded operators)
--------------------------------------------------------------------------------



特別な識別子を使っている関数宣言は、演算子関数(operator function)として認識される。この識別子は以下のようになる。



.. code-block:: c++
  
  operato

オーバーロード可能な演算子は以下の通りである。



.. code-block:: c++
  
  new     delete  new[]   delete[]
  +   -   *   /   %   ˆ   &   |   ~
  !   =   <   >   +=  -=  *=  /=  %=
  ˆ=  &=  |=  <<  >>  >>= <<= ==  !=
  <=  >=  &&  ||  ++  --  ,   ->* ->
  ( ) [ ]


以下の演算子は、単項、二項の両方でオーバーロードできる。


.. code-block:: c++
  
  +   -   *   &


以下の演算子は、関数呼び出しと添え字である。



.. code-block:: c++
  
  ( ) [ ]


以下の演算子は、オーバーロードできない。



.. code-block:: c++
  
  .   .*  ::  ?:


<p class="todo">
allocation functionとdeallocation functionへのリンク



演算子関数は、非staticメンバー関数か、非メンバー関数でなければならない。非staticメンバー関数の場合、暗黙のオブジェクト仮引数が、第一オペランドになる。これが*thisである。
非メンバー関数の場合、仮引数のひとつは、クラスか、クラスへのリファレンス、enumかenumへのリファレンスでなければならない。



.. code-block:: c++
  
  struct X
  {
      // 非staticメンバー関数による演算子関数
      X operator +() const ; // 暗黙のオブジェクト仮引数 X const &
      X operator +( int ) const ; // 暗黙のオブジェクト仮引数 X const &
  } ;
  
  // 非メンバー関数による演算子関数
  X operator -( X const & ) ;
  X operator -( X const &, int ) ;
  X operator -( int, X const & ) ;


以下の例はエラーである。



.. code-block:: c++
  
  // エラー、組み込みの演算子をオーバーロードできない
  int operator +( int, int ) ; 
  
  struct X { } ;
  // エラー、組み込みの演算子をオーバーロードできない
  X operator + ( X * ) ; 


ただし、代入演算子や添字演算子のように、非staticメンバー関数として実装しなければならない例外的な演算子もある。



演算子関数は、必ず元の演算子と同じ数の仮引数を取らなければならない。



.. code-block:: c++
  
  struct X　{　} ;
  
  X operator / ( X & ) ; // エラー、仮引数が少ない
  X operator / ( X &, X &, X & ) ; // エラー、仮引数が多い


ただし、これも関数呼び出し演算子のように、例外的な演算子がある。



演算子関数は、組み込みの演算子と同じ挙動を守らなくてもよい。例えば、戻り値の型は自由であるし、オーバーロードされた演算子関数が、基本型にその単項演算子を適用した場合に期待される挙動をしなくてもかまわない。例えば、オーバーロードした演算子関数では、"++a"、と、"a += 1"というふたつの式を評価した際の挙動や結果が同じにならなくてもよい。また、組み込み演算子ならば非constなlvalueを渡す演算子で、constなlvalueやrvalueを受け取っても構わない



.. code-block:: c++
  
  struct X　{　} ;
  
  void operator + ( X & ) ; // OK、戻り値の型は自由
  void operator ++ ( X const & ) ; // OK、constなlvalueリファレンスでもよい


演算子関数は、通常通り演算子を使うことによって呼び出すことができる。その際、演算子の優先順位は、組み込みの演算子と変わらない。また、識別子を指定することによって、通常の関数呼び出し式の文法で、明示的に呼び出すこともできる。



.. code-block:: c++
  
  struct X
  {
      X operator +( X const & ) const ;
      X operator *( X const & ) const ;
  } ;
  
  int main()
  {
      X a ; X b ; X c ;
      a + b ; // 演算子を使うことによる呼び出し
      a + b * c ; // 優先順位は、(a + (b * c))
  
      a.operator +(b) ; // 明示的な関数呼び出し
  }


代入演算子=や、単項演算子の&amp;や、カンマ演算子は、オーバーロードしなくてもすべての型に対してあらかじめ定義された挙動がある。この挙動はオーバーロードして変えることもできる。



単項演算子(Unary operators)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



オーバーロード可能な単項演算子は、以下の通りである。



.. code-block:: c++
  
  + - * & ~ ! 


ここでは、*と&amp;は単項演算子であることに注意。<a href="#over.binary">二項演算子</a>の項も参照。



インクリメント演算子とデクリメント演算子については、<a href="#over.inc">インクリメントとデクリメント</a>を参照。



単項演算子は、演算子を@とおくと、@xという式は、非staticメンバー関数の場合、x.operator @()、非メンバー関数の場合、operator @(x)として呼び出される。単項演算子では、非staticメンバー関数と非メンバー関数は、機能的に違いはない。



.. code-block:: c++
  
  struct X
  {
      void operator + () ;
  } ;
  
  void operator -( X & ) ;
  
  int main()
  {
      X x ;
      +x ; // x.operator + ()
      -x ; // operator + (x) 
  }


非staticメンバー関数の場合、明示的に仮引数をとらない。暗黙のオブジェクトが仮引数として渡される。



.. code-block:: c++
  
  struct X
  {
      void operator + () & ;
      void operator + () const & ;
      void operator + () volatile & ;
      void operator + () const volatile & ;
  
      void operator + () && ;
      void operator + () const && ;
      void operator + () volatile && ;
      void operator + () const volatile && ;
  } ;
  
  int main()
  {
      X x ;
      +x ; // void operator + () &
      +static_cast<X &&>(x) ; // void operator + () &&
  
      X const cx ;
      +x ; // void operator + () const &
  }


同様のコードを、非メンバー関数として書くと、以下のようになる。



.. code-block:: c++
  
  struct X { } ;
  
  void operator + ( X & ) ;
  void operator + ( X const & ) ;
  void operator + ( X volatile & ) ;
  void operator + ( X const volatile & ) ;
  
  void operator + ( X && ) ;
  void operator + ( X const && ) ;
  void operator + ( X volatile && ) ;
  void operator + ( X const volatile && ) ;
  
  int main()
  {
      X x ;
      +x ; // void operator + ( X & )
      +static_cast<X &&>(x) ; // void operator + ( X && )
  
      X const cx ;
      +x ; // void operator + ( X const & )
  }


また、非メンバー関数の場合は、クラス型を引数に取ることができる。



.. code-block:: c++
  
  struct X { } ;
  void operator + ( X ) ;


operator &amp;には、注意を要する。これは、組み込みの演算子、すなわち、オペランドのアドレスを得る演算子として、すべての型にあらかじめ定義されている。



.. code-block:: c++
  
  // operator &のオーバーロードなし
  struct X { } ;
  
  int main()
  {
      X x ;
      X * ptr = &x ; // 組み込みのoperator &の呼び出し
  }


この演算子をオーバーロードすると、組み込みのoperator &amp;が働かなくなる。



.. code-block:: c++
  
  struct X
  {
      X * operator &() { return nullptr ; }
  } ;
  
  int main()
  {
      X x ;
      X * ptr = &x ; // 常にnullポインターになる。
  }


もちろん、戻り値の型は自由だから、なにか別のことをさせるのも可能だ。



.. code-block:: c++
  
  class int_wrapper
  {
  private :
      int obj ;
  public :
      int * operator &() { return &obj ; } 
  } ;
  
  int main()
  {
      int_wrapper wrap ;
      int * ptr = &wrap ;
  }


ただし、クラスのユーザーが、オブジェクトのアドレスを得たい場合、組み込みの演算子を呼び出すのは簡単ではない。そのため、標準ライブラリヘッダー&lt;memory&gt;には、std::addressofという関数テンプレートが定義されている。これを使えば、operator &amp;がオーバーロードされているクラスでも、クラスのオブジェクトのアドレスを得ることができる。



.. code-block:: c++
  
  struct X
  {
      void operator &() { }
  } ;
  
  int main()
  {
      X x ;
      X * p1 = &x ; // エラー、operator &amp;の戻り値の型はvoid
      X * ptr = std::addressof(x) ; // OK
  }




二項演算子(Binary operators)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



オーバーロード可能な二項演算子は以下の通りである。



.. code-block:: c++
  
  +   -   *   /   %   ^   &   |   ~
  !   <   >   +=  -=  *=  /=  %=
  ^=  &=  |=  <<  >>  >>= <<= ==  !=
  <=  >=  &&  ||  ,


代入演算子は特別な扱いを受ける。詳しくは、<a href="#over.ass">代入演算子</a>を参照。複合代入演算子は、二項演算子に含まれる。



二項演算子は、演算子を@とおくと、x@yという式に対して、非staticメンバー関数の場合、x.operator @(y)、非メンバー関数の場合、operator @(x,y)のように呼び出される。



.. code-block:: c++
  
  struct X
  {
      void operator + (int) const ;
  } ;
  
  void operator - ( X const &, int ) ;
  
  int main()
  {
      X x ;
      x + 1 ; // x.operator +(1)
      x - 1 ; // operator -(1)
  }


非staticメンバー関数の場合、第一オペランドが暗黙のオブジェクト仮引数に、第二オペランドが実引数に渡される。



.. code-block:: c++
  
  struct X
  {
      void operator + (int) & ;
      void operator + (int) const & ;
      void operator + (int) volatile & ;
      void operator + (int) const volatile & ;
  
      void operator + (int) && ;
      void operator + (int) const && ;
      void operator + (int) volatile && ;
      void operator + (int) const volatile && ;
  } ;
  
  int main()
  {
      X x ;
      x + 1 ; // X::operator + (int) &
      static_cast<X &&>(x) + 1 ; // X::operator + (int) &&
      X const cx ;
      cx + 1 ; // X::operator + (int) const &
  }


同様のコードを、非メンバー関数で書くと以下のようになる。



.. code-block:: c++
  
  struct X { } ;
  
  void operator + ( X &, int) ;
  void operator + ( X const &, int) ;
  void operator + ( X volatile &, int) ;
  void operator + ( X const volatile &, int) ;
  
  void operator + ( X &&, int) ;
  void operator + ( X const &&, int) ;
  void operator + ( X volatile &&, int) ;
  void operator + ( X const volatile &&, int) ;
  
  int main()
  {
      X x ;
      x + 1 ; // operator + ( X &, int)
      static_cast<X &&>(x) + 1 ; // operator + ( X &&, int)
      X const cx ;
      cx + 1 ; // operator + ( X const &, int)
  }


非メンバー関数の場合は、クラス型を仮引数に取ることができる。



.. code-block:: c++
  
  struct X { } ;
  void operator + ( X, int ) ;


第二オペランドにクラスやenum型、あるいはそのリファレンス型を取りたい場合は、非メンバー関数しか使えない。



.. code-block:: c++
  
  struct X { } ;
  
  void operator + ( int, X & ) ;
  
  int main()
  {
      X x ;
      1 + x ;
  }


メンバー関数によるオーバーロードでは、必ず第一オペランドのメンバーとして演算子関数がよばれるので、これはできない。



カンマ演算子、operator ,には、あらかじめ定義された組み込みの演算子が存在する。オーバロードにより、この挙動を変えることもできる。ただし、operator ,の挙動を変えるのは、ユーザーを混乱させるので、慎むべきである。もし、単に任意個の引数を取りたいというのであれば、可変長テンプレートや初期化リストなどの便利な機能が他にもある。





代入(Assignment)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



代入演算子のオーバーロードは、仮引数をひとつとる非staticメンバー関数として実装する。非メンバー関数として実装することはできない。複合代入演算子は、代入演算子ではなく、二項演算子である。



.. code-block:: c++
  
  struct X
  {
      // コピー代入演算子
      X & operator = ( X const & ) ; 
      // ムーブ代入演算子
      X & operator = ( X && ) ;
  
      // intからの代入演算子
      X & operator = ( int ) ;
  } ;
  
  // エラー、非メンバー関数として宣言することはできない
  X & operator = ( X &, double ) ;
  
  // OK、複合代入演算子は二項演算子
  X & operator += ( X &, double ) ;


もちろん、戻り値の型は自由である。ただし、慣例として、暗黙に定義される代入演算子は、*thisを返すようになっている。詳しくは、<a href="#class.copy">クラスオブジェクトのコピーとムーブ</a>を参照。





関数呼び出し(Function call)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数呼び出し演算子の識別子は、operator ()である。関数呼び出し演算子のオーバーロードは、任意個の仮引数を持つ非staticメンバー関数として宣言する。非メンバー関数として宣言することはできない。デフォルト実引数も使うことができる。



関数呼び出し演算子は、x(arg1, ...)とおくと、x.operator()(arg1, ...)のように呼び出される。



.. code-block:: c++
  
  struct X
  {
      void operator () ( ) ;
      void operator () ( int ) ;
      void operator () ( int, int, int = 0 ) ;
  } ;
  
  int main()
  {
      X x ;
      x() ; // x.operator () ( )
      x( 0 ) ; // x.operator () ( 0 )
      x( 1, 2 ) ; // x.operator() ( 1, 2 ) 
  }




添字(Subscripting)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



添字演算子の識別子は、operator []である。添字演算子のオーバーロードは、ひとつの仮引数を持つ非staticメンバー関数として宣言する。非メンバー関数として宣言することはできない。



添字演算子は、x[y]とおくと、x.operator [] (y)のように呼び出される。



.. code-block:: c++
  
  struct X
  {
      void operator [] ( int ) ;
  } ;
  
  int main()
  {
      X x ;
      x[1] ; // x.operator [] (1)
  }


添字演算子に複数の実引数を渡すことはできない。ただし、初期化リストならば渡すことができる。



.. code-block:: c++
  
  struct X
  {
      void operator [] ( std::initializer_list<int> list ) ;
  } ;
  
  int main()
  {
      X x ;
      x[ { 1, 2, 3 } ] ;
  }




クラスメンバーアクセス(Class member access)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



クラスメンバーアクセス演算子の識別子は、operator -&gt;である。クラスメンバーアクセス演算子は仮引数を取らない非staticメンバー関数として宣言する。非メンバー関数にすることはできない。クラスメンバーアクセス演算子は、後述するように、少し変わった特徴がある。



クラスメンバーアクセス演算子は、x-&gt;mとおくと、(x.operator-&gt;())-&gt;mのように呼び出される。つまり、もし、x.operator-&gt;()の戻り値の型がクラスへのポインターであれば、そのまま組み込みのクラスメンバーアクセス演算子が使われる。それ以外の場合は、戻り値に対してクラスメンバーアクセス演算子を適用しているために、さらに戻り値のクラスメンバーアクセス演算子が、もし存在すれば、呼び出される。



.. code-block:: c++
  
  struct A 
  {
      int member ;
  } ;
  
  struct B
  {
      A a ;
      A * operator ->() { return &a ; }
  } ;
  
  struct C
  {
      B b ;
      B & operator ->() { return b ; }
  } ;
  
  
  int main()
  {
      B b ;
      b->member ; // (b.operator ->())->member
  
      C c ;
  // (c.operator ->())->member
  // すなわちこの場合、以下のように展開される。
  // ((c.operator ->()).operator ->())->member
      c->member ; 
  }


クラスBは、


クラスCのoperator -&gt;がB &amp;型を返していることに注目。lvalueのBにクラスメンバーアクセス演算子である-&gt;が使われるため、クラスBのクラスメンバーアクセス演算子が呼ばれる。



クラスメンバーアクセス演算子の評価の結果に対するクラスメンバーアクセス演算子の呼び出しは、際限なく行われる。このループを断ち切るには、最終的にクラスへのポインターを返し、組み込みのクラスメンバーアクセス演算子を使わなければならない。



もちろん、これは演算子として使用した場合であって、明示的に関数を呼び出す場合には、通常通り、その関数だけが呼ばれる。もちろん、戻り値の型をvoid型にすることもできる。



.. code-block:: c++
  
  struct X
  {
      void operator ->() { return nullptr ; }
  } ;
  
  
  int main()
  {
      X x ;
      x.operator ->() ; // OK
  }




インクリメントとデクリメント(Increment and decrement)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



インクリメント演算子の識別子はoperator ++、デクリメント演算子の識別子はoperator --である。インクリメント演算子とデクリメントの演算子は非staticメンバー関数と、非メンバー関数の両方で宣言できる。インクリメント演算子とデクリメント演算子は、識別子の違いを除けば、同じように動く。ここでのサンプルコードは、インクリメント演算子の識別子を使う。



インクリメントとデクリメントには、前置と後置の違いがある。



.. code-block:: c++
  
  ++a ; // 前置
  a++ ; // 後置


前置演算子は、非staticメンバー関数の場合、仮引数を取らない。非メンバー関数の場合は、ひとつの仮引数を取る。



前置演算子は、++xという式に対して、非staticメンバー関数の場合、x.operator ++ ()、非メンバー関数の場合、operator ++　( x )のように呼び出される。。



.. code-block:: c++
  
  struct X
  {// 非staticメンバー関数の例
      void operator ++ () ;
  } ;
  
  struct Y { } ;
  // 非メンバー関数の例
  void operator ++ ( Y & ) ;
  
  int main()
  {
      X x ;
      ++x ; // x.operator ++() 
  
      Y y ;
      ++y ; // operator ++(y) 
  }


後置演算子は、非staticメンバー関数の場合、int型の引数を取る。非メンバー関数の場合は、二つの仮引数を取る。第二仮引数の型はintでなければならない。int型の仮引数は、単に前置と後置を別の宣言にするためのタグであり、それ以上の意味はない。式としてインクリメントとデクリメントを使うと、実引数には0が渡される。



後置演算子は、x++という式に対して、非staticメンバー関数の場合、x.operator ++( 0 ), 非メンバー関数の場合、operator ++ ( x, 0 )のように呼び出される。



.. code-block:: c++
  
  struct X
  { // 非staticメンバー関数の例
      void operator ++ (int) ;
  } ;
  
  struct Y { } ;
  // 非メンバー関数の例
  void operator ++ ( Y & , int ) ;
  
  
  
  int main()
  {
      X x ;
      x++ ; // x.operator ++( 0 ) 
  
      Y y ;
      y++ ; // operator ++( y, 0 )
  }


intをタグとして使うこの仕様はすこし汚いが、例外的な文法を使わなくてもよいという利点があるので採用された。もし明示的に呼び出した場合は、int型の仮引数に対し、0以外の実引数を与えることもできる。





確保関数と解放関数(allocation function and deallocation function)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



<p class="todo">
Basic Conceptの該当項目の記述とリンク



注意：本来、これはコア言語ではなくライブラリで規定されていることなので、本書の範疇ではないのだが、ここでは読者の便宜のため、宣言方法と、デフォルトの挙動のリファレンス実装を提示する。また、サンプルコードは分割して掲載しているが、確保関数と解放関数はそれぞれ関係しており、すべて一つのソースファイルに含まれることを想定している。そのため、ヘッダーファイルのincludeは最初のサンプルコードにしか書いていない。



確保関数の識別子はoperator newである。解放関数の識別子はoperator deleteである。この関数は、動的ストレージの確保と解放を行う。確保関数と解放関数が行うのは、生の動的ストレージの確保と解放である。よく誤解があるが、コンストラクターやデストラクターの呼び出しの責任は持たない。



確保関数と解放関数のオーバーロードは、グローバル名前空間か、クラスのメンバー関数として宣言する。グローバル名前空間以外の名前空間で宣言するとエラーとなる。確保関数と解放感数がユーザー定義されない場合、実装によってデフォルトの挙動を行う確保関数と開放感数が自動的に定義される。



.. code-block:: c++
  
  // グローバル名前空間
  void* operator new(std::size_t size) ; // OK
  
  namespace NS
  {
  void* operator new(std::size_t size); // エラー、グローバル名前空間ではない
  }
  
  struct X
  {
      void* operator new(std::size_t size) ; // OK
  } ;


グローバル名前空間の宣言は、デフォルトの確保関数と解放関数の生成を妨げる。クラスのメンバー関数は、そのクラスと派生クラスの確保と解放に使われる。



確保関数には、効果(effect)と必須の挙動(required behavior)とデフォルトの挙動(default behavior)が規定されている。解放関数には、効果ととデフォルトの挙動が規定されている。効果とは、その関数がどのようなことに使われるのかという規定である。必須の挙動とは、たとえユーザー定義の関数であっても必ず守らなければならない挙動のことである。デフォルトの挙動とは、関数がユーザー定義されていない場合、実装によって用意される定義の挙動である。



C++11ではスレッドの概念が入ったので、確保関数と解放関数は、データ競合を引き起こしてはならない。この保証は、ユーザー定義の確保関数と開放感数にも要求される。



C++11ではアライメントの概念が入ったので、確保関数の確保するストレージは、要求されたサイズ以下の大きさのオブジェクトを配置できるよう、適切にアラインされていなければならない。




単数形の確保関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void* operator new(std::size_t size) ;


効果
  

必須の挙動
  

デフォルトの挙動
  



nothrow版の単数形の確保関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void * operator new( std::size_t size, const std::nothrow_t & ) noexcept ;


効果
  

必須の挙動
  

デフォルトの挙動
  



単数形の解放関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void operator delete( void * ptr ) noexcept ;


効果
  

デフォルトの挙動
  



nothrow版の単数形の解放関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void operator delete( void * ptr, const std::nothrow_t & ) noexcept ;


効果
  

デフォルトの挙動
  



配列形の確保関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void　* operator new[](　std::size_t size　)　;


効果
  

必須の挙動
  

デフォルトの挙動
  



nothrow版の配列形の確保関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void * operator new[]( std::size_t size, const std::nothrow_t & ) noexcept ;


効果
  

必須の挙動
  

デフォルトの挙動
  



配列型の解放関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void operator delete[]( void * ptr) noexcept ;


効果
  

デフォルトの挙動
  



nothrow版の配列型の解放関数
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  void operator delete[]( void * ptr, const std::nothrow_t & ) noexcept ;


効果
  

デフォルトの挙動
  





ユーザー定義リテラル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



<p class="todo">
Basic Conceptsの該当項目へのリンク



以下の形のオーバーロード演算子は、ユーザー定義リテラル演算子のオーバーロードである。



.. code-block:: c++
  
  operator "" 識別子


""と識別子の間には、必ずひとつ以上の空白文字を入れなければならない。また、識別子の先頭文字は、必ずアンダースコアひとつから始まらなければならない。ただし、通常の識別子では、アンダースコアから始まる名前は予約されているので注意すること。これは、ユーザー定義リテラル演算子のみの特別な条件である。



.. code-block:: c++
  
  // OK
  void operator "" /* 空白文字が必要 */ _x( unsigned long long int ) ;
  
  // エラー、""と_yの間に空白文字がない
  void operator ""_y( unsigned long long int ) ;
  
  // エラー、識別子がアンダースコアから始まっていない
  void operator "" z( unsigned long long int ) ;
  
  // エラー、""の間に空白文字がある
  void operator " " _z( unsigned long long int ) ;


リテラル演算子の仮引数リストは、以下のいずれかでなければならない。



.. code-block:: c++
  
  const char*
  unsigned long long int
  long double
  char
  wchar_t
  char16_t
  char32_t
  const char*, std::size_t
  const wchar_t*, std::size_t
  const char16_t*, std::size_t
  const char32_t*, std::size_t


上記以外の仮引数リストを指定すると、エラーとなる。



リテラル演算子テンプレートは、仮引数リストが空で、テンプレート仮引数は、char型の非型テンプレート仮引数の仮引数パックでなければならない。



.. code-block:: c++
  
  template < char ... Chars >
  void operator "" _x () { }


これ以外のテンプレート仮引数を取るリテラル演算子テンプレートはエラーとなる。



リテラル演算子は、Cリンケージを持つことができない。



.. code-block:: c++
  
  // エラー
  extern "C" void operator "" _x( unsigned long long int ) { }
  
  // OK
  extern "C++" void operator "" _x( unsigned long long int ) { }


リテラル演算子は、名前空間スコープで宣言しなければならない。つまり、クラススコープで宣言することはできない。ただし、friend関数になることはできる。



.. code-block:: c++
  
  // グローバル名前空間スコープ
  void operator "" _x( unsigned long long int ) { }
  
  namespace ns {
  // ns名前空間スコープ
  void operator "" _x( unsigned long long int ) { }
  }
  
  class X
  {
      // OK、friend宣言できる
      friend void operator "" _x( unsigned long long int ) ;
  
      // エラー、クラススコープでは宣言できない
      static void operator "" _y( unsigned long long int ) ; 
  } ;


ただし、名前空間スコープで宣言したリテラル演算子を、ユーザー定義リテラルとして使うには、using宣言かusingディレクティブが必要となる。



.. code-block:: c++
  
  namespace ns {
  void operator "" _x( unsigned long long int ) { }
  }
  
  int main( )
  {
      1_x ; // エラー、operator "" _xは見つからない
  
      {
          using namespace ns ;
          1_x ; // OK
      }
  
      {
          using ns::operator "" _x ;
          1_x ; // OK
      }
  }


これ以外は、通常の関数と何ら変りない。例えば、明示的に呼び出すこともできるし、その際には通常のオーバーロード解決に従う。inlineやconstexpr関数として宣言することもできる。内部リンケージでも外部リンケージのどちらでも持てる。アドレスも取得できる。等々。





