クラス（Classes）
================================================================================

トリビアルにコピー可能なクラス（trivially copyable class）
--------------------------------------------------------------------------------



トリビアルにコピー可能なクラス（trivially copyable class）とは、クラスのオブジェクトを構成するバイト列の値を、そのままコピーできるクラスのことである。詳しくは、<a href="#basic.types">型</a>を参照。



あるクラスがtrivially copyable classとなるには、以下の条件をすべて満たさなければならない。



非trivialな、コピーコンストラクター、ムーブコンストラクター、コピー代入演算子、ムーブ代入演算子を持たないこと。trivialなデストラクターを持っていること。



つまり、これらの特別なメンバー関数を、ユーザー定義してはならない。また、virtual関数やvirtual基本クラスも持つことはできない。trivialの詳しい定義については、<a href="#class.copy">クラスオブジェクトのコピーとムーブ</a>を参照。



ここで、「持たない」ということは、delete定義によって削除しても構わないということである。



.. code-block:: c++
  
  struct A
  {
      A( A const & ) =delete ;
      A( A && ) = delete ;
      A & operator = ( A const & ) = delete ;
      A & operator = ( A && ) = delete ;
  
      // trivialなデストラクターは、「持って」いなければならない
  
      int x ;
  } ;


また、アクセス指定子が異なるメンバーを持っていても構わない。



上記のクラスAは、コピーもムーブもできないクラスであるが、trivially copyable classである。


トリビアルクラス（trivial class）
--------------------------------------------------------------------------------



トリビアるクラス（trivial class）とは、trivially copyable classの条件に加えて、trivialなデストラクターを持っているクラスである。


標準レイアウトクラス（standard-layout class）
--------------------------------------------------------------------------------



標準レイアウトクラス（standard-layout class）の詳しい説明については、<a href="#class.mem">クラスのメンバー</a>を参照。



あるクラスが標準レイアウトクラスとなるためには、以下の条件をすべて満たさなければならない。



標準レイアウトクラスではない非staticメンバーをもたない。また、そのようなクラスへの配列やリファレンスも持たない。



virtual関数とvirtual基本クラスを持たない。



非staticデータメンバーは、すべて同じアクセス指定子である。



.. code-block:: c++
  
  // 標準レイアウトクラス
  struct S
  {
  // すべて同じアクセス指定子
      int x ;
      int y ;
      int z ;
  
  // staticデータメンバーは、別のアクセス指定子でもよい
  private :
      int data ;
  } ;
  int S:data ;


標準レイアウトクラスではないクラスを基本クラスに持たない。



基本クラスに非staticデータメンバーがある場合は、クラスは非staticデータメンバーを持たない。クラスが非staticデータメンバーを持つ場合は、基本クラスは非staticデータメンバーを持たない。つまり、クラスとその基本クラス（複数可）の集合の中で、どれかひとつのクラスだけが、非staticなデータメンバーを持つことが許される。



.. code-block:: c++
  
  struct Empty { } ;
  struct Non_empty { int member ; } ;
  
  // 以下は標準レイアウトクラス
  struct A
  // 基本クラスに非staticデータメンバーがある場合
      : Non_empty
  {
  // 非staticデータメンバーを持たない
  } ;
  
  struct B
  // 基本クラスは非staticデータメンバーを持たない
      : Empty
  {
  // 非staticデータメンバーを持つ場合
      int data ;
  } ;
  
  // 以下は標準レイアウトクラスではない
  // 基本クラスもクラスCも非staticデータメンバーを持っている
  struct C
      : Non_empty
  {
      int data ;
  } ;


最初の非staticデータメンバーと、基本クラスとで、同じ型を使わない。



.. code-block:: c++
  
  // 標準レイアウトクラスではない例
  struct A { } ;
  struct B
  // 基本クラス
      : A
  {
      A a ; // 最初の非staticデータメンバー
      int data ;
  } ;
  
  // 最初の非staticデータメンバーでなければよい
  struct C : A
  {
      int data ;
      A a ;
  } ;


この制限は、基本クラスとデータメンバーとの間で、アドレスが重複するのを防ぐためである。



.. code-block:: c++
  
  struct A { } ;
  struct B : A { A a ; } ;
  
  B obj ;
  
  A * p1 = &obj ; // 基本クラスのサブオブジェクトへのアドレス
  A * p2 = &obj.a ; // データメンバーへのアドレス
  
  // p1 != p2が保証される


このような場合、もし、クラスBが標準レイアウトクラスであれば、基本クラスのサブオブジェクトへのアドレスと、データメンバーのサブオブジェクトへのアドレスが重複してしまう。つまり、p1とp2が同じ値になってしまう。異なるアドレスを得られるためには、このようなクラスを標準レイアウトクラスにすることはできない。



標準レイアウトクラスのうち、structとclassのキーワードで定義されるクラスを、特に標準レイアウトstructと言う。unionキーワードで定義されるクラスを、特に標準レイアウトunionという。


POD構造体（POD struct）
--------------------------------------------------------------------------------



PODとは、Plain Old Dataの略である。これは、C言語の構造体に相当するクラスである。C++11では、クラスがPODの条件を満たした際に保証される動作を、trivially copyable classと、標準レイアウトクラスの二つの動作に細分化した。そのため、C++11では、特にPODにこだわる必要はない。



クラスがPODとなるためには、trivial classと標準レイアウトクラスの条件を満たし、さらに、PODではないクラスを非staticデータメンバーに持たないという条件が必要になる。


クラス名（Class names）
--------------------------------------------------------------------------------



TODO:あまり深く解説しなくてもいい気がする。


クラスのメンバー（Class members）
--------------------------------------------------------------------------------



クラスのメンバー指定には、宣言文、関数の定義、using宣言、static_assert宣言、テンプレート宣言、エイリアス宣言を書くことができる。



.. code-block:: c++
  
  struct Base { int value ; } ;
  
  struct S : Base
  {
      int data_member ; // 宣言文
      void member_function() { } // 関数の定義
      using Base::value ; // using宣言
      static_assert( true, "this must not be an error." ) ; // static_assert宣言
      template < typename T > struct Inner { } ; // テンプレート宣言
      using type = int ; // エイリアス宣言
  } ;


このうち、クラスのメンバーとなるのは、データメンバーとメンバー関数、ネストされた型名、列挙子である。



.. code-block:: c++
  
  struct S
  {
      int x ; // データメンバー
      void f() { } ; // メンバー関数
      using type = int ; // ネストされた型名
      enum { id } ; // 列挙子
  } ;


データメンバーは、俗にメンバー変数とも呼ばれている。クラス定義内で、変数の宣言文を書くと、データメンバーとなる。



クラスのメンバーを、クラスの定義内で複数回宣言することはできない。ただし、クラス内のクラスとenumに関しては、前方宣言することができる。



.. code-block:: c++
  
  class Outer
  {
      void f() ;
      void f() ; // エラー、複数回の宣言
  
      class Inner ; // クラス内クラスの宣言
      class Inner { } ; // OK、クラス内クラスの定義
  
      enum struct E : int ; // クラス内enumの宣言
      enum struct E : int { id } ; // OK、クラス内enumの定義
  } ;


クラスは、}で閉じた所をもって、完全に定義されたとみなされる。たとえ、メンバー関数が定義されていなくても、クラス自体は完全に定義された型となる。



<p class="editorial-note">
TODO: クラス定義内で完全型になる例外も書くべきか？



メンバーはコンストラクターで初期化できる。詳しくは<a href="#class.ctor">コンストラクター</a>を参照。メンバーは初期化子で初期化できる。詳しくは、<a href="#class.static.data">staticデータメンバー</a>と、<a href="#class.base.init">基本クラスとデータメンバーの初期化</a>を参照。



.. code-block:: c++
  
  struct S
  {
      S() : x(0) { } // コンストラクター
      int x = 0 ; // 初期化子
      static int data ;
  } ;
  
  int S::data = 0 ; // 初期化子


メンバーは、externやregister指定子と共に宣言することはできない。メンバーをthread_local指定子と共に宣言する場合は、static指定子も指定しなければならない。



.. code-block:: c++
  
  struct S
  {
      extern int a ; // エラー
      register int b ; // エラー
      thread_local int c ; // エラー
  
      // OK、staticと共に宣言している
      static thread_local int d ;
  } ;
  
  thread_local int S::d ; // 定義


基本的に、クラス名と同じ名前のメンバーを持つことはできない。これには、一部の例外が存在するが、本書では解説しない。



.. code-block:: c++
  
  struct name
  {
      static int name ;       // エラー
      void name() ;           // エラー
      static void name() ;    // エラー
      using name = int ;      // エラー
      enum { name } ;         // エラー    
      union { int name } ;    // エラー
  } ;


unionではないクラスにおいて、同じアクセス指定下にある非staticデータメンバーは、クラスのオブジェクト上で、宣言された順番に確保される。つまり、先に宣言されたデータメンバーは、後に宣言されたデータメンバーよりも、上位のアドレスに配置される。ただし、実装は必要なパディングを差し挟むかもしれないので、後のデータメンバーが、先のデータメンバーの直後に配置されるという保証はない。



.. code-block:: c++
  
  struct S
  {
  public :
  // 同じアクセス指定下にある非staticデータメンバー
      int x ;
      int y ;
  } ;
  
  int main()
  {
      S s ;
      int * p1 = &s.x ;
      int * p2 = &s.y ;
  
      // この式は、必ずtrueとなる
      p1 < p2 ;
      // この式がtrueとなる保証はない
      p1 + 1 == p2 ;
  }


アクセス指定子が異なる非staticデータメンバーの配置に関しては、未規定である。



標準レイアウトstructのオブジェクトへのポインターは、reinterpret_castによって変換された場合、クラスの最初のメンバーへのポインターに変換できる。また、その逆も可能である。



.. code-block:: c++
  
  struct S { int x ; } ;
  
  int main()
  {
      S s ;
      S * p1 = &s ;
      int * p2 = &s.x ;
  
      // 以下の2式は、trueとなることが保証されている
      p1 == reinterpret_cast< S * >( p2 ) ;
      p2 == reinterpret_cast< int * >( p1 ) ;
  }


レイアウト互換（layout-compatible）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



レイアウト互換（layout-compatible）という概念がある。まず、同じ型は、レイアウト互換である。



もし、二つの標準レイアウトstructが、同じ数の非staticデータメンバーを持ち、対応する非staticデータメンバーが、それぞれレイアウト互換であったならば、そのクラスは、お互いにレイアウト互換structである。



もし、二つの標準レイアウトunionが、同じ数の非staticデータメンバーを持ち、対応する非staticデータメンバーが、それぞれレイアウト互換であったならば、そのクラスは、お互いにレイアウト互換unionである。



二つの標準レイアウトstructは、レイアウト互換structのメンバーが続く限り、オブジェクト上で共通の表現をしていると保証される。



.. code-block:: c++
  
  // A、Bは、2番目のメンバーまで、お互いにレイアウト互換
  struct A
  {
      int x ;
      int y ;
      float z ;
  } ;
  
  struct B
  {
      int x ;
      int y ;
      double z ;
  } ;
  
  int main()
  {
      A a ;
  
      B * ptr = reinterpret_cast< B * >( &a ) ;
      // OK、aのオブジェクトの、対応するレイアウト互換なメンバーが変更される
      ptr->x = 1 ;
      ptr->y = 2 ;
     
      // エラー、3番目のメンバーは、レイアウト互換ではない
      ptr->z = 0.0 ;
  }


ただし、メンバーがビットフィールドの場合、お互いに同じビット数でなければならない。



.. code-block:: c++
  
  // AとBはお互いにレイアウト互換
  struct A
  {
      int x:8 ;
  } ;
  struct B
  {
      int x:8 ;
  } ;


標準レイアウトunionが、お互いにレイアウト互換な複数の標準レイアウトstructを持つとき、先頭から共通のメンバーについては、一方を変更して、他方で使うこともできる。



.. code-block:: c++
  
  struct A
  {
      int x ;
      int y ;
      float z ;
  } ;
  
  struct B
  {
      int x ;
      int y ;
      double z ;
  } ;
  
  union U
  {
      A a ;
      B b ; 
  } ;
  
  int main()
  {
      U u ;
      u.a.x = 1 ;
      u.a.y = 2 ;
  
      // 以下の2式はtrueとなることが保証されている
      u.b.x == 1 ;
      u.b.y == 2 ;
  
      // 3番目のメンバーは、レイアウト互換ではない
  }




メンバー関数（Member functions）
--------------------------------------------------------------------------------



クラスの定義内で宣言される関数を、クラスのメンバー関数（member function)という。メンバー関数はstatic指定子と共に宣言することができる。その場合、関数はstaticメンバー関数となる。staticメンバー関数ではないメンバー関数のことを、非staticメンバー関数という。ただし、friend指定子と共に宣言された関数は、メンバー関数ではない。



.. code-block:: c++
  
  struct S
  {
      void non_static_member_function() ; // 非staticメンバー関数
      static void static_member_function() ; // staticメンバー関数
  
      friend void friend_function() ; // これはメンバー関数ではない
  } ;


メンバー関数は、クラス定義の内側でも外側でも定義することができる。クラス定義の内側で定義されたメンバー関数を、inlineメンバー関数という。これは、暗黙的にinline関数となる。クラス定義の外側でメンバー関数を定義する場合、クラスと同じ名前空間スコープ内で定義しなければならない。



.. code-block:: c++
  
  struct S
  {
      // inlineメンバー関数
      void inline_member_function()
      { /*定義*/ }
  
      void member_function() ; // メンバー関数の宣言
  } ;
  
  // クラスSと同じ名前空間スコープ
  void S::member_function()
  { /*定義*/ }


クラス定義の外側でinlineメンバー関数の定義をすることもできる。それには、関数宣言か関数定義で、inline指定子を使えばよい。



.. code-block:: c++
  
  struct S
  {
      inline void f() ; 
      void g() ;
  } ;
  
  void S::f(){ }
  inline void S::g() { }


クラス定義の外側でメンバー関数を定義するためには、メンバー関数の名前を、::演算子によって、クラス名で修飾しなければならない。



.. code-block:: c++
  
  struct S
  {
      void member() ;
  } ;
  
  void S::member(){ }


<a href="#class.local">ローカルクラス</a>では、メンバー関数をクラス定義の外側で宣言する方法はない。



非staticメンバー関数（Nonstatic member functions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



非staticメンバー関数は、そのメンバー関数が属するクラスや、そのクラスから派生されたクラスのオブジェクトに対して、<a href="#expr.ref">クラスメンバーアクセス演算子</a>を使うことで、呼び出すことができる。同じクラスや、そのクラスから派生されたクラスのメンバー関数からは、他のメンバー関数を、通常の関数の呼び出しと同じように呼ぶことができる。



.. code-block:: c++
  
  struct Object
  {
      void f(){ }
      void g()
      {
          // 関数呼び出し
          f() ;
      }
  } ;
  
  int main()
  {
      Object object ;
      // クラスのメンバーアクセス演算子と、関数呼び出し
      object.f() ;
  }


非staticメンバー関数は、CV修飾子と共に宣言することができる。



.. code-block:: c++
  
  struct S
  {
      void none() ;
      void c() const ; // constメンバー関数
      void v() volatile ; // volatileメンバー関数
      void cv() const volatile ; // const volatileメンバー関数
  } ;


このCV修飾子は、thisポインターの型を変える。また、メンバー関数の型も、CV修飾子に影響される。



非staticメンバー関数は、リファレンス修飾子と共に宣言することができる。リファレンス修飾子は、オーバーロード解決の際の、暗黙の仮引数の型に影響を与える。詳しくは、<a href="#over.match.funcs">候補関数と実引数リスト</a>を参照。



非staticメンバー関数は、virtualやピュアvirtualの文法で宣言することができる。詳しくは、<a href="#class.virtual">virtual関数</a>や、<a href="#class.abstract">抽象クラス</a>を参照。




thisポインター（The this pointer）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



非staticメンバー関数内では、thisというキーワードが、クラスのオブジェクトへのprvalueのポインターを表す。このクラスのオブジェクトは、メンバー関数を呼び出した際のクラスのオブジェクトである。



.. code-block:: c++
  
  struct Object
  {
      void f()
      {
          this ;
      }
  } ;
  
  
  int main()
  {
      Object a, b, c ;
  
      a.f() ; // thisは&a
      b.f() ; // thisは&b
      c.f() ; // thisは&c
  }


class Xのメンバー関数におけるthisの型は、X *である。もし、constメンバー関数の場合、X const *となり、volatileメンバー関数の場合、X volatile *となり、const volatileメンバー関数の場合は、X const volatile *となる。



.. code-block:: c++
  
  class X
  {
      // thisの型はX *
      void f() { this ; }
      // thisの型はX const *
      void f() const { this ; }
      // thisの型はX volatile *
      void f() volatile { this ; }
      // thisの型はX const volatile *
      void f() const volatile { this ; }
  } ;


constメンバー関数では、メンバー関数に渡されるクラスのオブジェクトがconstであるため、thisの型も、constなクラスへのポインター型となり、非staticデータメンバーを変更することができない。



.. code-block:: c++
  
  class X
  {
      int value ;
  
      void f() const
      {
          this->value = 0 ; // エラー
      }
  } ;


これは、thisの型を考えてみると分かりやすい。



.. code-block:: c++
  
  class X
  {
      int value ;
  
  
      void f() const
      {
          X const * ptr = this ;
          ptr->value = 0 ; // エラー
      }
  } ;


thisの型が、constなクラスに対するポインターなので、データメンバーを変更することはできない。



同様にして、volatileの場合も、非staticデータメンバーはvolatile指定されたものとみなされる。volatileの具体的な機能ついては、実装に依存する。



CV修飾されたメンバー関数は、同等か、より少なくCV修飾されたクラスのオブジェクトに対して呼び出すことができる。



.. code-block:: c++
  
  struct X
  {
      X() { }
      void f() const { } ;
  } ;
  
  int main()
  {
      X none ;
      none.f() ; // OK、より少なくCV修飾されている
      X const c ;
      c.f() ; // OK、同じCV修飾
  
      X const volatile cv ;
      cv.f() ; // エラー、CV修飾子を取り除くことはできない
  }


これは、非staticメンバー関数から、他の非staticメンバー関数を、クラスメンバーアクセスなしで呼び出す際にも当てはまる。その場合、クラスのオブジェクトとは、thisである。



.. code-block:: c++
  
  struct X
  {
      void c() const // constメンバー関数
      {
          // thisの型はX const *
          nc() ; // エラー、CV修飾子を取り除くことはできない
      } ;
  
      void nc() // 非constメンバー関数
      {
          // thisの型はX *
          c() ; // OK、CV修飾子を付け加えることはできる
      }
  } ;


コンストラクターとデストラクターは、CV修飾子と共に宣言することができない。ただし、これらの特別なメンバー関数は、constなクラスのオブジェクトの生成、破棄の際にも、呼び出される。




staticメンバー（Static members）
--------------------------------------------------------------------------------



クラスのデータメンバーやメンバー関数は、クラス定義内で、static指定子と共に宣言することが出来る。そのように宣言されたメンバーを、クラスのstaticメンバーという。



.. code-block:: c++
  
  struct S
  {
      static int data_member ;
      static void member_function() ; 
  } ;
  int S::data_member ;


クラスXのstaticメンバーsは、::演算子を用いて、X::sのように参照することで、使うことができる。staticメンバーは、クラスのオブジェクトがなくても参照できるので、クラスのメンバーアクセス演算子を使う必要はない。しかし、クラスのメンバーアクセス演算子を使っても参照できる。



.. code-block:: c++
  
  struct X
  {
      static int s ;
  } ;
  
  int X::s ;
  
  int main()
  {
      // ::演算子による参照
      X::s ;
  
      // クラスのメンバーアクセス演算子でも参照することはできる
      X object ;
      object.s ;
  }


クラスのメンバー関数内では、非修飾名を使った場合、クラスのstaticメンバー、enum名、ネストされた型が名前探索される。



.. code-block:: c++
  
  struct X
  {
      void f()
      {
          s ; // X::s
          value ; // X::value
          type obj ; // X::type
      }
  
      static int s ;
      enum { value } ;
      typedef int type ;
  } ;
  int X::s ;


staticメンバーにも、通常通りのアクセス指定が適用される。



staticメンバー関数（Static member functions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



staticメンバー関数は、thisポインターを持たない。virtual指定子を使えない。CV修飾子を使えない。名前と仮引数の同じ、staticメンバー関数と非staticメンバー関数は、両立できない。



.. code-block:: c++
  
  struct S
  {
      // エラー、同じ名前と仮引数のstatic関数と非static関数が存在する
      void same() ;
      static void same() ; 
  } ;


その他は、通常のメンバー関数と同じである。




staticデータメンバー（Static data members）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



staticデータメンバーは、クラスのサブオブジェクトには含まれない。staticデータメンバーは、クラスのスコープでアクセス可能なstatic変数だと考えてもよい。クラスのすべてのオブジェクトは、ひとつのstaticデータメンバーのオブジェクトを共有する。ただし、static thread_localなデータメンバーのオブジェクトは、スレッドにつきひとつ存在する。



.. code-block:: c++
  
  struct S
  {
      static int member ;
  } ;
  int S::member ;
  
  int main()
  {
      S a, b, c, d, e ;
      // すべて同じオブジェクトを参照する
      a.member ; b.member ; c.member ; e.member ;
  }


クラス定義内のstaticデータメンバー宣言は、定義ではない。staticデータメンバーの定義は、クラスの定義を含む名前空間スコープの中に書かなければならない。その際、名前に::演算子を用いて、クラス名を指定する必要がある。staticデータメンバーの定義には、初期化子を使うことができる。初期化子は必須ではない。



.. code-block:: c++
  
  struct S
  {
      static int member ;
  } ;
  
  // クラス名 :: メンバー名
  void S::member = 0 ;


staticデータメンバーが、constなリテラル型の場合、クラス定義内の宣言に、初期化子を書くことができる。この場合、初期化子は定数式でなければならない。staticデータメンバー自体も、定数式になる。初期化子を書かない場合は、通常通り、クラス定義の外、同じ名前空間スコープ内で、定義を書かなければならない。この場合は、定数式にはならない。



.. code-block:: c++
  
  struct S
  {
      static const int constant_expression = 123 ; // 定数式
      static const int non_constant_expression ; // 宣言、定数式ではない
  } ;
  const int S::non_constant_expression = 123 ; // 定義


リテラル型のstaticデータメンバーは、constexpr指定子をつけて宣言することもできる。この場合、初期化子を書かなければならない。初期化子は、定数式でなければならない。このように定義されたstaticデータメンバーは、定数式になる。



.. code-block:: c++
  
  struct S
  {
      static constexpr int constant_expression = 123 ; // 定数式
  } ;


名前空間スコープのクラスのstaticデータメンバーは、外部リンケージを持つ。ローカルクラスのstaticデータメンバーは、リンケージを持たない。



staticデータメンバーは、非ローカル変数と同じように、初期化、破棄される。詳しくは、<a href="#basic.start.init">非ローカル変数の初期化</a>、<a href="#basic.start.term">終了</a>を参照。



staticデータメンバーには、mutable指定子は使えない。




union（Unions）
--------------------------------------------------------------------------------



<p class="editorial-note">
TODO: variant memberに書き換え。



unionというクラスは、クラスキーにunionキーワードを用いて宣言する。unionでは、非staticデータメンバーは、どれかひとつのみが有効である。これは、unionのオブジェクト内では、非staticデータメンバーのストレージは、共有されているからである。unionのサイズは、非staticデータメンバーのうち、最も大きな型を格納するのに十分なサイズとなる。



.. code-block:: c++
  
  union U
  {
      int i ;
      short s ;
      double d ;
  } ;
  
  int main()
  {
      U u ;
      u.i = 0 ; // U::iが有効
      u.s = 0 ; // U::sが有効、U::iは有効ではなくなる
  
  }


この例では、unionのサイズは、int, short, doubleのうちの、最もサイズが大きな型を格納するのに十分なだけのサイズである。データメンバーであるi, s, dは、同じストレージを共有している。



unionと、標準レイアウトクラスについては、<a href="#class">クラス</a>を参照。



unionは、通常のクラスに比べて、いくらか制限を受ける。unionはvirtual関数を持つことができない。unionは、基本クラスを持つことができない。unionは基本クラスになれない。unionは、リファレンス型の非staticデータメンバーを持つことができない。unionの非staticデータメンバーのうち、初期化子を持てるのは、ひとつだけである。



.. code-block:: c++
  
  // エラーの例
  
  // エラー、virtual関数を持てない
  union U1 { virtual void f() { } } ;
  // エラー、基本クラスを持てない
  struct Base { } ;
  union U : Base { } ;
  // エラー、基本クラスになれない
  union Union_base { } ;
  union Derived : Union_base { } ;
  // エラー、リファレンス型の非staticデータメンバーを持てない
  uion U2 { int & ref ; } ;
  // エラー、非staticデータメンバーで、初期化子を持てるのは、ひとつだけ
  
  union U3
  {
      int x = 0 ; 
      int y = 0 ; // エラー、複数の初期化子、どちらか一つならエラーではない
  } ;


その他は、通常のクラスと変わることがない。unionはメンバー関数を持てる。メンバー関数には、コンストラクターやデストラクター、演算子のオーバーロードも含まれる。アクセス指定も使える。staticデータメンバーならば、リファレンス型でも構わない。ネストされた型も使える。



unionの非staticデータメンバーが、非trivialなコンストラクター、コピーコンストラクター、ムーブコンストラクター、コピー代入演算子、ムーブ代入演算子、デストラクターを持っている場合、unionの対応するメンバーが、暗黙的にdeleteされる。そのため、これらのメンバーを使う場合には、union側で、ユーザー定義しなければならない。



.. code-block:: c++
  
  union U
  {
      std::string str ;
      std::vector<int> vec ;
  } ;
  
  int main()
  {
      U u ; // エラー、コンストラクターとデストラクターがdelete定義されている。
  }


この例では、strやvecは、非trivialなコンストラクターやデストラクターなどを持っているので、union側でも、それらを定義しなければならない。また、この例の場合、unionのコンストラクターやデストラクターは何もしないので、このunionを実際に使う場合には、placement newや、明示的なデストラクター呼び出しが必要になる。



.. code-block:: c++
  
  union U
  {
      std::string str ;
      std::vector<int> vec ;
  
      U() { }
      ~U() { }
  } ;
  
  int main()
  {
      U u ;
  
      new ( &u.str ) std::string( "hello" ) ;
      u.str.~basic_string() ;
  
      new ( &u.vec ) std::vector<int> { 1, 2, 3 } ;
      u.vec.~vector() ;
  }


もちろん、unionのコンストラクターやデストラクターで、どれかのデータメンバーの初期化、破棄をすることは可能である。しかし、どのデータメンバーが有効なのかということを、union内で把握するのは難しい。



無名union（anonymous union）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



以下のような形式のunionの宣言を、無名union（anonymous union）という。



.. code-block:: c++
  
  union { メンバー

無名unionは、無名の型のunionの、無名のオブジェクトを生成する。無名unionのメンバー指定は、非staticデータメンバーだけでなければならない。無名unionのメンバーの名前は、宣言されているスコープの他の名前と衝突してはならない。無名unionでは、staticデータメンバーやメンバー関数、ネストされた型などは使えない。また、privateやprotectedアクセス指定も使えない。



.. code-block:: c++
  
  int main()
  {
      union { int i ; short s ; } ;
      // iかsのどちらかひとつだけが有効
      i = 0 ;
      s = 0 ;
  }


これは、以下のようなコードと同じであると考えることもできる。



.. code-block:: c++
  
  int main()
  {
      union Anonymous { int i ; short s ; } unnamed ;
      unnamed.i = 0 ;
      unnamed.s = 0 ;
  }


名前空間スコープで宣言される無名unionには、必ずstatic指定子をつけなければならない。



.. code-block:: c++
  
  // グローバル名前空間スコープ
  static union { int x ; int y ; } ;


名前空間スコープで宣言される無名unionは、staticストレージの有効期間と、内部リンケージを持つ。



ブロックスコープで宣言される無名unionは、ブロックスコープ内で許されているすべてのストレージ上に構築できる。



.. code-block:: c++
  
  int main()
  {
      // 自動ストレージ
      union { int a } ;
      // staticストレージ
      static union { int b } ;
      // thread_localストレージ
      thread_local union { int c } ;
  }


クラススコープで宣言される無名unionには、ストレージ指定子を付けることはできない。



.. code-block:: c++
  
  struct S
  {
      union
      {
          int x ;
      } ;
  } ;


オブジェクトやポインターを宣言している、クラス名の省略されたunionは、無名unionではない。



.. code-block:: c++
  
  // クラス名の省略されたunion
  // 無名unionではない
  union { int x ; } obj, * ptr ;




共用メンバー（variant member）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



union、もしくは無名unionを直接のメンバーに持つクラスを、unionのようなクラス（union-like class）という。unionのようなクラスには、共用メンバー（variant member）という概念が存在する。unionの共用メンバーは、unionの非staticデータメンバーである。無名unionを直接のメンバーに持つクラスの場合、無名unionの非staticデータメンバーである。



.. code-block:: c++
  
  // xとyは共用メンバー
  union U { int x ; int y ; }
  
  // xとyは共用メンバー
  struct S
  {
      union { int x ; int y ; } ;
  } ;




ビットフィールド（Bit-fields）
--------------------------------------------------------------------------------



ビットフィールドは、以下のようなメンバー宣言子の文法で宣言できる。



.. code-block:: c++
  
  識

定数式は、0よりも大きい整数でなければならない。



.. code-block:: c++
  
  struct S
  {
      int // 型指定子
      x : 8 ; // ビットフィールドの宣言子
  } ;


ビットフィールドの定数式は、データメンバーのサイズをビット数で指定する。ビットフィールドに関しては、ほとんどの挙動が実装依存である。特に、ビットフィールドがクラスオブジェクトのストレージ上でどのように表現されるのかということや、アライメントなどは、すべて実装依存である。また、実装は、ビットフィールドのメンバー同士を詰めて表現することが許されている。



.. code-block:: c++
  
  struct S
  {
      char x : 1 ;
      char y : 1 ;
  } ;


ここで、sizeof(S)は、2以上になるとは限らない。例えば、sizeof(S)が1を返す実装もあり得る。



ビットフィールドの定数式は、オブジェクトのビット数を上回ることができる。その場合、上回ったビット数は、パディングとして確保されるが、オブジェクトの内部表現として使われることはない。



.. code-block:: c++
  
  struct S
  {
      int x : 1000 ;
  } ;


ここで、sizeof(S)は、少なくとも1000ビット以上になる値を返す（規格では、1バイトあたりのビット数は定められていない）。ただし、X::sは、本来のint型以上の範囲の値を保持することはできない。int型のオブジェクトのビット数を上回った分は、単にパディングとして確保されているに過ぎない。



ビットフィールドの宣言子で、識別子を省略した場合、無名ビットフィールドとなる。無名ビットフィールドはクラスのメンバーではなく、初期化もされない。ただし、実装依存の方法で、クラスのオブジェクト内に存在する。一般的な実装では、無名ビットフィールドは、オブジェクトのレイアウトを調整するためのパディングとして用いられる。



.. code-block:: c++
  
  struct S
  {
      int x : 4 ;
      char : 3 ; // 無名ビットフィールド
      int y : 1 ;
  } ;


あるコンパイラーでは、このような無名ビットフィールドにより、S::xとS::yの間に、3ビット分のパディングを挿入することができる。ただし、すでに述べたように、ビットフィールドの内部表現とアライメントは実装依存なので、これはすべてのコンパイラーに当てはまるわけではない。使用しているコンパイラーが、ビットフィールドをどのように実装しているかは、コンパイラー独自のマニュアルを参照すべきである。



無名ビットフィールドでは、特別に、定数式に0を指定することができる。



.. code-block:: c++
  
  struct S
  {
      int x : 4 ;
      char : 0 ; // 無名ビットフィールド
      int y : 4 ;
  } ;


これは、無名ビットフィールドの次のビットフィールドのアライメントを、アロケーション単位の境界に配置させるための指定である。上記の構造体は、ある環境では、S::xとS::yが同一のアロケーション単位に配置されるかもしれないが、無名ビットフィールドを使うことで、X::yを別のアロケーション単位に配置できる。



<p class="editorial-note">
TODO:構造体のオブジェクトの内部表現を視覚化した図




ビットフィールドはstaticメンバーにはできない。ビットフィールの型は、整数型かenum型でなければならない。符号が指定されていない整数型のビットフィールドの符号は実装依存である。



.. code-block:: c++
  
  struct S
  {
      static int error : 8 ; // エラー、ビットフィールドはstaticメンバーにはできない
      int impl : 8 ; // 符号は実装依存
      signed s : 8 ; // 符号はsigned
      unsigned u : 8 ; // 符号はunsigned
  } ;


bool型のビットフィールドは、ビット数に関わらず、bool型の値を表現できる。



.. code-block:: c++
  
  struct S
  {
      bool a : 1 ;
      bool b : 2 ;
      bool c : 3 ;
  } ;
  
  int main()
  {
      S s ;
      s.a = true ;
      s.b = false ;
      s.c = true ;
  }


ビットフィールドのアドレスを得ることはできない。つまり、&amp;演算子をビットフィールドに適用することはできない。



.. code-block:: c++
  
  struct S
  {
      int x : 8 ;
  } ;
  
  int main()
  {
      S s ;
      &s.x ; // エラー
  }


リファレンスは、ビットフィールドを参照することはできない。ただし、constなlvalueリファレンスの初期化子が、lvalueのビットフィールドの場合は、一時オブジェクトが生成され、そのオブジェクトを参照する



.. code-block:: c++
  
  struct S
  {
      int x : 8 ;
  } ;
  
  int main()
  {
      S s ;
      // エラー
      int & ref = s.x ;
      // OK
      // ただし、crefが参照するのは、生成された一時オブジェクトである
      // s.xではない
      int const & cref = s.x ;
  }


クラス宣言のネスト（Nested class declarations）
--------------------------------------------------------------------------------



クラスは、他のクラスの内側で宣言することができる。これを、ネストされたクラス（nested class）という。



.. code-block:: c++
  
  class Outer
  {
      class Inner { } ; // ネストされたクラス
  } ;
  
  int main()
  {
      Outer::Inner object ;
  }


ネストされたクラスのスコープは、外側のクラスのスコープに従う。これは、名前探索の際も、外側のクラスのスコープが影響するということである。



.. code-block:: c++
  
  int x ; // グローバル変数
  
  struct Outer
  {
      int x ; // Outer::x
      struct Inner
      {
          void f()
          {
              sizeof(x) ; // OK、sizeofのオペランドは未評価式。Outer::xのサイズを返す
              x = 0 ; // エラー、Outer::xはOuterの非staticメンバー
  
              ::x = 0 ; // OK、グローバル変数
          }
      } ;
  } ;


関数Inner::fの中で、xという名前を使うと、Outer::xが見つかる。これは、クラスInnerが、クラスOuterのスコープ内にあるためである。しかし、非staticデータメンバーであるOuter::xを使うためには、Outerのオブジェクトが必要なので、ここではエラーとなる。sizeofのオペランドは未評価式なので、問題はない。ただし、ここでのxは、Outer::xである。グローバル変数のxではない。



ネストされたクラスのメンバー関数やstaticデータメンバーは、通常のクラス通り、クラス定義の外側、同じ名前空間内で定義することができる。



.. code-block:: c++
  
  // グローバル名前空間
  struct Outer
  {
  
      struct Inner
      {
          static int x ;
          void f() ;
      } ;
  } ;
  
  // 同じ名前空間内
  int Outer::Inner::x = 0 ;
  void Outer::Inner::f() { }


また通常通り、クラスの宣言だけをして、定義を後で書くこともできる。



.. code-block:: c++
  
  struct Outer
  {
      class Inner ; // 宣言
  } ;
  
  class Outer::Inner { } ; // 定義


ローカルクラス宣言（Local class declarations）
--------------------------------------------------------------------------------



関数定義の中で、クラスを定義することができる。これをローカルクラス（local class）という。



.. code-block:: c++
  
  int main()
  { // 関数定義
      class Local { } ; // ローカルクラス
      Local object ; // ローカルクラスのオブジェクト
  }


ローカルクラスのスコープは、クラス定義の外側のスコープである。また、名前探索は、ローカルクラスが定義されている関数と同じとなる。



ローカルクラスは、定義されている関数内の自動変数を使うことは出来ない。typedef名やstatic変数などは使える。



.. code-block:: c++
  
  int main()
  {
      int x ; // ローカル変数
  
      typedef int type ;
      static int y ;
  
      class Local
      {
          void f()
          {
              x = 0 ; // エラー
  
              // typedef名やstatic変数などは使える
              type val ; // OK
              y = 0 ; // OK
  
              // OK、sizeofのオペランドは未評価式
              sizeof(x) ;
          }
      } ;
  }


ローカルクラスは、通常のクラスより制限が多い。ローカルクラスをテンプレート宣言することはできない。メンバーテンプレートを持つこともできない。ローカルクラスのメンバー関数は、クラス定義内で定義されなければならない。ローカルクラスの外側でメンバー関数を定義する方法はない。staticデータメンバーを持つことはできない。



.. code-block:: c++
  
  int main()
  {
      // エラー、ローカルクラスはテンプレート宣言できない
      template < typename T > 
      class Local
      {
          // エラー、ローカルクラスはメンバーテンプレートを持てない。
          template < typename U > void f() { } 
  
          // OK、ただし、ローカルクラスの外側でメンバー関数を定義する方法はない
          void f() ;
          // エラー、ローカルクラスはstaticデータメンバーを持つことはできない。 
          static int x ;
      } ;
  }


型名のネスト（Nested type names）
--------------------------------------------------------------------------------



クラス内の型名を、ネストされた型名（nested type name）という。ネストされた型名を、クラスの外側で使うには、クラス名による修飾が必要である。



.. code-block:: c++
  
  struct X
  {
      typedef int I ;
      class Inner { } ;
      I member ;
  } ;
  
  X::I object ;


