メンバーのアクセス指定（Member access control）
================================================================================

アクセス指定子（Access specifiers）
--------------------------------------------------------------------------------



クラスのメンバーのアクセス指定は、ラベルにアクセス指定子（Access specifiers）を記述することで指定する。



.. code-block:: c++
  
  アクセス指定子 : メンバー

アクセス指定子とは、private、protected、publicのいずれかである。アクセス指定子が現れた場所から、次のアクセス指定子か、クラス定義の終了までの間のメンバーが、アクセス指定子の影響を受ける



class X
{
    int a ; // デフォルトのprivate
public :
    int b ; // public
    int c ; // public
protected :
    int d ; // protected
private :
    int e ; // private
} ;



アクセス指定子には、順番や使用可能な回数の制限はない。好きな順番で、何度でも指定できる。



.. code-block:: c++
  
  class X
  {
  public :
  public :
  protected :
  public :
  public :
  private :
  } ;


基本クラスと、基本クラスのメンバーへのアクセス指定（Accessibility of base classes and base class members）
--------------------------------------------------------------------------------



あるクラスを、別のクラスの基本クラスとするとき、いずれかのアクセス指定子を指定する。



.. code-block:: c++
  
  class Base { } ;
  
  class Derived_by_public : public Base { } ; // public派生
  class Derived_by_protected : protected Base { } ; // protected派生
  class Derived_by_private : private Base { } ; // private派生


アクセス指定子がpublicの場合、基本クラスのpublicメンバーは、派生クラスのpublicメンバーとしてアクセス可能になり、基本クラスのprotectedメンバーは、派生クラスのprotectedメンバーとしてアクセス可能になる。



.. code-block:: c++
  
  class Base
  {
  public :
      int public_member ;
  protected :
      int protected_member ;
  } ;
  
  class Derived : public Base
  {
      void f()
      {
          public_member ; // OK
          protected_member ; // OK
      }
  } ;
  
  int main()
  {
      Derived d ;
      d.public_member ; // OK
  }


アクセス指定子がprotectedの場合、基本クラスのpublicとprotectedメンバーは、派生クラスのprotectedメンバーとしてアクセス可能になる。



.. code-block:: c++
  
  class Base
  {
  public :
      int public_member ;
  protected :
      int protected_member ;
  } ;
  
  class Derived : protected Base
  {
      void f()
      {
          public_member ; // OK、ただしprotectedメンバー
          protected_member ; // OK
      }
  } ;
  
  int main()
  {
      Derived d ;
      d.public_member ; // エラー、Derivedからは、protectedメンバーである
  }


アクセス指定子がprivateの場合、基本クラスのpublicとprotectedメンバーは、派生クラスのprivateメンバーとしてアクセス可能になる。



.. code-block:: c++
  
  class Base
  {
  public :
      int public_member ;
  protected :
      int protected_member ;
  } ;
  
  class Derived : private Base
  {
      void f()
      {
          public_member ; // OK、ただし、privateメンバー
          protected_member ; // OK、ただし、privateメンバー
      }
  } ;
  
  class Derived2 : public Derived
  {
      void f()
      {
          public_member ; // エラー、基本クラスのprivateメンバーにはアクセスできない
          protected_member ; // エラー、基本クラスのprivateメンバーにはアクセスできない
      }
  } ;
  
  int main()
  {
      Derived d ;
      d.public_member ; // エラー、Derivedからは、privateメンバーである
  }


基本クラスにアクセス指定子を指定しなかった場合、structキーワードで宣言されたクラスは、デフォルトでpublicに、classキーワードで宣言されたクラスは、デフォルトでprivateになる。



.. code-block:: c++
  
  struct Base { } ;
  
  // デフォルトのpublic派生
  struct D1 : Base { } ; 
  // デフォルトのprivate派生
  class D2 : Base { } ;


どのアクセス指定子を指定して派生しても、基本クラスのprivateメンバーを派生クラスから使うことはできない。クラスAからprivate派生したクラスBから派生しているクラスCでは、クラスAのメンバーは使えないのも、この理由による。



.. code-block:: c++
  
  // classキーワードで宣言されたクラスのメンバーはデフォルトでprivate
  class Base { int private_member ; } ;
  
  class Derived : public Base
  {
  // どのアクセス指定を用いても、基本クラスのprivate_memberは使えない
  } ;
  
  struct A { int public_member ; } ;
  class B : private A { } ;
  class C : public B
  {
  // クラスBは、クラスAからprivate派生しているため、ここではA::public_memberは使えない。
  } ;


クラス名自体も、クラススコープ内の名前として扱われる。クラスAからprivate派生したクラスBから派生しているクラスCでは、クラスAのクラス名自体がprivateメンバーになってしまう。



.. code-block:: c++
  
  // グローバル名前空間のスコープ
  struct A { } ;
  class B : private A { } ;
  class C : public B
  {
      void f()
      {
          A a1 ; // エラー、名前Aは、基本クラスのprivateメンバーのA
          ::A a2 ; // OK、名前::Aは、グローバル名前空間スコープ内のA
      }
  } ;


この例では、クラスCのスコープ内で、非修飾名Aに対して、クラス名Aが発見されてしまうので、エラーになる。クラスCの中でクラスAを使いたい場合、明示的な修飾が必要である。



アクセス指定子は、staticメンバーにも適用される。publicなstaticメンバーを持つクラスを、protectedやprivateで派生すると、基本クラスからはアクセスできるが、派生クラスを介してアクセスできなくなってしまうこともある。



.. code-block:: c++
  
  // グローバル名前空間のスコープ
  struct A { static int data ; } ;
  int A::data ; 
  
  class B : private A { } ;
  class C : public B
  {
      void f()
      {
          data ; // エラー
          ::A::data ; // OK
      }
  } ;


クラスCからは、名前dataは、基本クラスAのメンバーdataとして発見されるので、アクセスできない。しかし、クラスA自体は、名前空間に存在するので、明示的な修飾を使えば、アクセスできる。



protectedの場合、friendではないクラス外部の関数からアクセスできなくなる。



.. code-block:: c++
  
  struct A { static int data ; }
  int A::data ;
  
  class B : protected A { } ;
  
  int main()
  {
      B::data ; // エラー
      A::data ; // OK
  }


ここでは、B::dataとA::dataは、どちらも同じオブジェクトを指しているが、アクセス指定の違いにより、B::dataという修飾名では、クラスBのfriendではないmain関数からアクセスすることができない。



基本クラスにアクセス可能である場合、派生クラスへのポインター型から、基本クラスへのポインター型に型変換できる。



.. code-block:: c++
  
  class A { } ;
  class B : public A { } ;
  class C : protected A
  {
      void f()
      {
          static_cast< A * >( this ) ; // OK、アクセス可能
      }
  } ;
  
  int main()
  {
      B b ;  
      static_cast< A * >( &b ) ; // OK、アクセス可能
      C c ;
      static_cast< A * >( &c ) ; // エラー、main関数からは、protectedメンバーにアクセスできない
      
  }


friend（Friends）
--------------------------------------------------------------------------------



クラスはfriendを宣言することができる。friendを宣言するには、friend指定子を使う。クラスのfriendとして宣言できるものは、関数かクラスである。クラスのfriendは、クラスのprivateとprotectedメンバーにアクセスできる。



.. code-block:: c++
  
  class X
  {
  private :
      typedef int type ; // privateメンバー
      friend void f() ; // friend関数
      friend class Y ; // friendクラス
  } ;
  
  void f()
  {
      X::type a ; // OK、関数void f(void)はXのfriend
  }
  
  class Y
  {
      X::type member ; // OK、クラスYはXのfriend
      void f()
      {
          X::type member ; // OK、クラスYはXのfriend        
      }
  } ;


friendクラスの宣言は、friend指定子に続けて、<a href="#dcl.type.elab">複雑型指定子</a>、<a href="#dcl.type.simple">単純型指定子</a>、typename指定子（<a href="#temp.res">名前解決</a>を参照）のいずれかを宣言しなければならない。



複雑型指定子は、最も分かりやすい。



.. code-block:: c++
  
  class X
  {
      friend class Y ;
      friend struct Z ;
  } ;


複雑型指定子を使う場合、クラスをあらかじめ宣言しておく必要はない。名前がクラスであることが、その時点で宣言されるからだ。



単純型指定子に名前を使う場合は、それより以前に、クラスを宣言しておく必要がある。



.. code-block:: c++
  
  class Y ; // Yをクラスとして宣言
  
  class X
  {
      friend Y ; // OK、Yはクラスである
      friend Z ; // エラー、名前Zは見つからない
  
      friend class A ; // OK、Aはクラスとして、ここで宣言されている
  } ;


あらかじめ名前が宣言されていない場合は、エラーとなる。



単純型指定子にテンプレート名を使うこともできる。



.. code-block:: c++
  
  template < typename T >
  class X
  {
      friend T ; // OK
  } ;


typename指定子を指定する場合は、以下のようになる。



.. code-block:: c++
  
  template < typename T >
  class X
  {
      friend typename T::type ;
  } ;


T::typeは、依存名を型として使っているので、typenameが必要である。



もし、型指定子がクラス型ではない場合、単に無視される。これは、テンプレートコードを書くときに便利である。



.. code-block:: c++
  
  template < typename T >
  class X
  {
      friend T ;
  } ;
  
  X<int> x ; // OK、friend宣言は無視される
  
  template < typename T >
  class Y
  {
      friend typename T::type ;
  } ;
  
  struct Z { typedef int type ; } ;
  
  Y<Z> y ; // OK、friend宣言は無視される


無視されるのは、あくまで、型指定子がクラス型ではなかった場合である。すでに説明したように、単純型指定子で、名前が見つからなかった場合は、エラーになる。



friend関数の宣言は、通常通りの関数の宣言の文法に、friend指定子を記述する。前方宣言は必須ではない。friend関数には、<a href="#dcl.stc">ストレージクラス指定子</a>を記述することはできない。



.. code-block:: c++
  
  class X
  {
      friend void f() ;
      friend int g( int, int, int ) ;
      friend X operator + ( X const &, X const & ) ;
  } ;


friend関数として宣言された関数がオーバーロードされていた場合でも、friend関数として宣言したシグネチャの関数しか、friendにはならない。



.. code-block:: c++
  
  void f( int ) ;
  void f( double ) ;
  
  class X
  {
      friend void f( int ) ;
  } ;


この例では、void f(int)のみが、Xのfriend関数になる。void f(double)は、friend関数にはならない。



他のクラスのメンバー関数も、friend関数として宣言できる。メンバー関数には、コンストラクターやデストラクターも含まれる。



.. code-block:: c++
  
  class X ; // 名前Xをクラス型として宣言
  
  class Y
  {
  public :
      void f( ) ; // メンバー関数
      Y & operator = ( X const & ) ; // 代入演算子
      Y() ; // コンストラクター
      ~Y() ; // デストラクター
  } ;
  
  class X
  {
      // 以下4行は、すべて正しいfriend宣言
      friend void Y::f( ) ;
      friend Y & Y::operator = ( X const & ) ;
      friend Y::Y() ;
      friend Y::~Y() ;
  } ;


friend宣言自体には、アクセス指定は適用されない。ただし、friend宣言の中でアクセスできない名前を使うことはできない。



.. code-block:: c++
  
  class Y
  {
  private :
      void f( ) ; // privateメンバー
  } ;
  
  class X
  {
      // エラー、Yのprivateメンバーにはアクセス出来ない
      // friend宣言の中の名前の使用には、アクセス指定が影響する
      friend void Y::g() ;
  
  // アクセス指定は、friend宣言自体に影響を及ぼさない
  // 以下3行のfriend宣言に、アクセス指定は何の意味もなさない
  private :
      friend void f() ;
  protected :
      friend void g() ;
  public :
      friend void h() ;
  } ;


Y::fはprivateメンバーなので、Xからはアクセスできない。Xのfriend宣言は、関数f, g, hを、Xのfriendとして宣言しているが、この宣言に、Xのアクセス指定は何の効果も与えない。



friend宣言は、実は関数を定義することができる。



.. code-block:: c++
  
  class X
  {
      friend void f() { } // 関数の定義
  } ;


friend宣言で定義された関数は、クラスが定義されている名前空間スコープの関数になる。クラスのメンバー関数にはならない。ただし、friend宣言で定義された関数は、ADLを使わなければ、呼び出すことはできない。非修飾名前探索や、修飾名前探索で、関数名を参照する方法はない。



.. code-block:: c++
  
  // グローバル名前空間のスコープ
  
  class X
  {
      // fはメンバー関数ではない
      // クラスXの定義されているグローバル名前空間のスコープ内の関数
      friend void f( X ) { }
      // gはメンバー関数ではない
      // gを呼び出す方法は存在しない
      friend void g() { }
  } ;
  
  int main()
  {
      X x ;
      f(x) ; // OK、ADLによる名前探索
  
      (f)(x) ; // エラー、括弧がADLを阻害する。ADLが働かないので名前fが見つからない
      ::f(x) ; // エラー、名前fが見つからない
      g() ; // エラー、名前gが見つからない
  }


このように、通常の名前探索では関数名が見つからないという問題があるため、friend宣言内での関数定義は、行うべきではない。




friendによって宣言された関数は、前方宣言されていない場合、外部リンケージを持つ。前方宣言されている場合、リンケージは前方宣言に従う。



.. code-block:: c++
  
  inline void g() ; // 前方宣言、関数gは内部リンケージを持つ
  
  class X
  {
      friend void f() ; // 関数fは外部リンケージを持つ
      friend void g() ; // 関数gは内部リンケージを持つ
  } ;
  
  // 定義
  void f() { } // 外部リンケージ
  inline void g() { }


friend宣言は、派生されることはない。また、あるクラスのfriendのfriendは、あるクラスのfriendではない。つまり、友達の友達は、友達ではない。



.. code-block:: c++
  
  class A
  {
  private :
      typedef int type ;
      friend class B ;
  } ;
  
  class B
  {
      // OK、BはAのfriend
      typedef A::type type ;
  
      friend class C ;
  } ;
  
  class C
  {
      // エラー、BはAのfriendである。CはBのfriendである。
      // Cは、Aからみて、friendのfriendにあたる。
      // しかし、CはAのfriendではない。
      typedef A::type type ;
  } ;
  
  class D : public B
  {
      // エラー、DはBから派生している。BはAのfriendである。
      // しかし、DはAのfriendではない
      typedef A::type type ;
  } ;


ローカルクラスの中でfriend宣言で、非修飾名を使った場合、名前探索において、ローカルクラスの定義されている関数外のスコープは考慮されない。friend関数を宣言する場合、対象の関数はfriend宣言に先立って宣言されていなければならない。friendクラスを宣言する場合、クラス名はローカルクラスの名前であると解釈される。



.. code-block:: c++
  
  class A ; // ::A
  void B() ; // ::B
  
  void f()
  {
      // 関数の前方宣言は関数内でも可能
      void C( void ) ; // 定義は別の場所
  
      class Y ; // ローカルクラスYの宣言
  
      // ローカルクラスXの定義
      class X
      {
          friend class A ; // OK、ただし、::Aではなく、ローカルクラスのA
          friend class ::A ; // OK、::A
          friend class Y ; // OK、ただしローカルクラスY
  
          friend void B() ; // エラー、Bは宣言されていない。::Bは考慮されない
          friend void C() ; // OK、関数内の前方宣言により名前を発見
      } ;
  }


friend宣言とテンプレートの組み合わせについては、<a href="#temp.friend">テンプレート宣言のfriend</a>を参照。


protectedメンバーアクセス（Protected member access）
--------------------------------------------------------------------------------



<p class="editorial-note">
TODO:保留


virtual関数へのアクセス（Access to virtual functions）
--------------------------------------------------------------------------------



virtual関数へのアクセスは、virtual関数の宣言によって決定される。virtual関数のオーバーライドには影響されない。



.. code-block:: c++
  
  class Base
  {
  public :
      virtual void f() { }
  } ;
  
  class Derived : public Base
  {
  private :
      void f() { } // Base::fをオーバーライド
  } ;
  
  int main()
  {
      Derived d ;
      d.f() ; // エラー、Derived::fはprivateメンバー
  
      Base & ref = d ;
      ref.f() ; // OK、Derived::fを呼ぶ
  }


Derived::fはprivateメンバーなので、関数mainから呼び出すことはできない。しかし、Base::fはpublicメンバーである。Base::fはvirtual関数なので、呼び出す関数は、実行時のオブジェクトの型によって決定される。この時、オーバーライドしたvirtual関数のアクセス指定は、考慮されない。Base::fのアクセス指定のみが考慮される。この例では、関数mainから、Derived::fを直接呼び出すことはできないが、Baseへのリファレンスやポインターを経由すれば、呼び出すことができる。



virtual関数呼び出しのアクセスチェックは、呼び出す際の式の型によって、静的に決定される。基本クラスでpublicメンバーとして宣言されているvirtual関数を、派生クラスでprotectedやprivateにしても、基本クラス経由で呼び出すことができる。


複数のアクセス（Multiple access）
--------------------------------------------------------------------------------



多重派生によって、基本クラスのメンバーに対して、複数のアクセスパスが形成されている場合、アクセス可能なパスを経由してアクセスが許可される。



.. code-block:: c++
  
  class Base
  {
  public :
      void f() { }
  } ;
  
  class D1 : private virtual Base { } ;
  class D2 : public virtual Base { } ;
  
  class Derived : public D1, public D2
  {
      void f()
      {
          Base::f() ; // OK、D2を経由してアクセスする
      }
  } ;


D1はBaseをprivate派生しているので、DerivedからD1経由では、Baseにアクセスできない。しかし、D2経由でアクセスできる。


ネストされたクラス（Nested classes）
--------------------------------------------------------------------------------



ネストされたクラスも、クラスのメンバーであるので、他のメンバーとアクセス権限を持つ。



.. code-block:: c++
  
  class Outer
  {
  private :
      typedef int type ; // privateメンバー
  
      class Inner
      {
          Outer::type data ; // OK、InnerはOuterのメンバー
      } ;
  } ;


OuterにネストされたクラスInnerは、Outerのメンバーなので、Outerのprivateメンバーにアクセスすることができる。



ただし、ネストされたクラスをメンバーとして持つクラスは、ネストされたクラスに対して、特別なアクセス権限は持たない。



.. code-block:: c++
  
  class Outer
  {
      class Inner
      {
      private :
          typedef int type ; // privateメンバー
      } ;
  
      void f()
      {
          Inner::type x ; // エラー、Inner::typeはprivateメンバー
      }
  } ;


この例では、Outerは、Innerのprivateメンバーにはアクセスできない。


