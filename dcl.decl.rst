宣言子（Declarators）
================================================================================

型名（Type names）
--------------------------------------------------------------------------------



キャスト、sizeof、alignof、new、typeidでは、型の名前を指定する。これには、型名が用いられる。型名とは、変数や関数を宣言する場合と同じ指定子と宣言子だが、名前を省略したものである。



.. code-block:: c++
  
  int value ;         // int型の変数
  int                 // 型名
  int array[10] ;     // 配列型の変数
  int [10]            // 型名
  int (*p)(void) ;    // 関数ポインター型の変数
  int (*)(void)       // 型名


ただし、あまりにも複雑な型名は、typedefやエイリアス宣言でtypedef名を定義した方が分かりやすい。


曖昧解決（Ambiguity resolution）
--------------------------------------------------------------------------------



宣言文は、文法上、曖昧になる場合がある。これは、通常気にする必要はない。ただし、まれにこの曖昧性に引っかかり、不可解なコンパイルエラーを引き起こす可能性がある。



仮引数名に無駄な括弧のある関数の宣言と、初期化式に関数形式のキャストを用いた変数の宣言は曖昧である。その場合、=が使われていると、初期化であるとみなされる。また、仮引数の周りの不必要な括弧は取り除かれる。その結果、変数の宣言のつもりで書いたコードが、関数の宣言とみなされてしまうことがある。



.. code-block:: c++
  
  struct S { S(int) { } } ;
  
  int main()
  {
      double d = 0.0 ;
  
      S w( int(d) ); // S(int)型の関数の宣言、dは仮引数名、無駄な括弧
      S x( int() ); // S(int)型の関数の宣言、仮引数名の省略、無駄な括弧
  
      S y( static_cast<>(d) ); // S型の変数yの宣言
      S z = int(d); // S型の変数zの宣言
  }


一般に、この曖昧解決の結果、変数を宣言したいのに、関数の宣言とみなされてしまい、コンパイルエラーになることがある。この文法上の曖昧性を避けるためには、static_castなどの他のキャストを使うか、=を使った初期化に書き換える必要がある。



関数形式のキャストと型名は、曖昧になることがある。例えば、int()というコードは、関数形式のキャストにも、int(void)型の関数の型名にも解釈できる。この場合、型名が期待される場所では、常に型名として解釈される。



.. code-block:: c++
  
  template < int N > struct C { } ;
  
  int main()
  {
      int x = int() ; // OK、intは関数形式のキャスト
      C<int()> ; // エラー、int()は型名
      C<int(0)> ; // OK
      
      sizeof(int()) ; // エラー、int()は型名
      sizeof(int(0)) ; // OK
  }


宣言子の意味（Meaning of declarators）
--------------------------------------------------------------------------------



<a href="#dcl.simple-declaration">単純宣言</a>は、指定子と宣言子で構成される。



.. code-block:: c++
  
  指定子 宣言子 ;


宣言子は、必ず、識別子を持たなければならない。この識別子を、規格上では、宣言識別子（declarator-id）と名付けている。この識別子は、宣言される名前となる。



.. code-block:: c++
  
  int name1 ; // name1はint型の変数の名前
  int * name2 ; // name2 はint *型の変数の名前
  int name3(void) ; // name3 はint (void)型の関数の名前


static, thread_local, extern, register, mutable, friend, inline, virtual, typedefといった指定子は、この宣言子の識別子に適用される。



宣言子の識別子の意味は、指定子と宣言子の組み合わせによって決定される。



.. code-block:: c++
  
  // 識別子aはint型の変数
  int     // 指定子
  a ;     // 宣言子、
  // 識別子bはint型のtypedef名
  typedef int // 指定子
  c ;         // 宣言子


変数、関数、型は、すべてこの指定子と宣言子の組み合わせによって宣言される。宣言子は、識別子の他にも、様々な文法があり、それによって、指定子の型を変更する。これには、ポインター、リファレンス、メンバーへのポインター、配列、関数、デフォルト実引数がある。



ポインター（Pointers）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



宣言子が以下のように記述されている場合、ポインターを意味する。



.. code-block:: c++
  
  * CV修

.. code-block:: c++
  
  int * a ; // intへのポインター型


*に続くCV修飾子は、ポインター型に対するCV修飾子として解釈される。



int * constは、指定子intへのポインターに対するconstである。intに対するconstではない。const int *とint const *はどちらも同じ型である。const intもint constも指定子だからだ。



.. code-block:: c++
  
  typedef const int * type1 ;
  typedef int const * type2 ;
  typedef int * const type3 ;


このように宣言されている場合、type1とtype2は同じ型である。type3は、type1やtype2とは別の型である。



宣言子の中に、ポインターは複数書くことができる。



.. code-block:: c++
  
  int obj ;
  int * p = &obj ;
  int * * pp = &p ;
  int * * * ppp = &pp ;
  
  int const * * a ; // int const *へのポインター
  int * const * b ; // int * constへのポインター
  int * * const c = nullptr ; // int *へのconstなポインター


T * *という型は、T *へのポインターということになる。



リファレンスへのポインターは存在しない。



.. code-block:: c++
  
  int & * ptr_to_ref ; // エラー、リファレンスへのポインターは存在しない


ビットフィールドのアドレスを取得することは禁止されているので、ビットフィールドへのポインターも存在しない。



関数へのポインターや、配列へのポインターは存在する。ただし、記述がやや難しい。コードの可読性を挙げるために、これらの型や変数を宣言するには、typedefやエイリアス宣言、autoなどを使うという手もある。



.. code-block:: c++
  
  void func( void ) { } // 型はvoid (void)
  
  void g()
  {
      void (*ptr_func)( void ) = &func ;
      ref_func() ; // 関数呼び出し
  
      int array[5] ; // 型はint [5]
      int (*ptr_array)[5] = &array ;
  }




リファレンス（References）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



宣言子が以下のように記述されている場合、リファレンスを意味する。



.. code-block:: c++
  
  & 識別子
  && 識別子


&amp;の場合、lvalueリファレンスとなり、&amp;&amp;の場合、rvalueリファレンスとなる。lvalueリファレンスとrvalueリファレンスは、ほとんど同じ働きをする。単にリファレンスといった場合、lvalueリファレンスとrvalueリファレンスの両方を指す。



.. code-block:: c++
  
  void f( int obj )
  {
      int & lvalue_reference = obj ;
      int && rvalue_reference = static_cast< int && >( obj ) ;
  
      lvalue_reference = 0 ; // objに0を代入
      rvalue_reference = 0 ; // objに0を代入
  }


リファレンスは、CV修飾できない。



.. code-block:: c++
  
  void f( int obj )
  {
      int const & a = obj ; // OK、int constへのリファレンス
      int & const b = obj ; // エラー、リファレンスへのCV修飾はできない
  }


ただし、typedefやテンプレート実引数にCV修飾子が使われた場合は、単に無視される。



.. code-block:: c++
  
  // typedefの例
  void f( void )
  {
      int const & a = 3 ; // OK、int constへのリファレンス
      typedef int & type ;
      typedef const type type2 ; // type2の型はint &
      const type b = 3 ; // エラー、bの型はint &
  }
  
  // テンプレート実引数の例
  template < typename T >
  struct S
  {
      typedef const T type ; 
  } ;
  
  void g()
  {
      typedef S< int & >::type type ; // type はint &
  }


typedefの例では、typeというtypedef名にconst修飾子が使われているが、これは単に無視される。したがって、bの型は、int &amp;である。int &amp; constとはならないし、int const &amp;ともならない。



テンプレートの例では、テンプレート仮引数Tの実際の型が決定されるのは、テンプレート実引数が渡されて、インスタンス化されたときである。



void型へのリファレンスは存在しない。



.. code-block:: c++
  
  typedef void & type ; // エラー


リファレンスへのリファレンス、リファレンスの配列、リファレンスへのポインターは存在しない。



.. code-block:: c++
  
  typedef int & & type1 ; // エラー、リファレンスへのリファレンス
  typedef int & type2[5] ;   // エラー、リファレンスの配列
  typedef int & * type3 ;     // エラー、リファレンスへのポインター


その他の型へのリファレンスは存在する。例えば、配列へのリファレンスや、関数へのリファレンスは存在する。ただし、ポインターと同じく、記述がやや難しい。



.. code-block:: c++
  
  void func( void ) { } // 型はvoid (void)
  
  void g()
  {
      void (&ref_func)( void ) = func ;
      ref_func() ; // 関数呼び出し
  
      int array[5] ; // 型はint [5]
      int (&ref_array)[5] = array ;
  }


リファレンスの宣言には、<a href="#dcl.init">初期化子</a>が必要である。



.. code-block:: c++
  
  void f()
  {
      int obj ;
  
      int & ref1 ; // エラー、初期化子がない
      int & ref2 = obj ; // OK
  }


ただし、宣言がextern指定子を含む場合、クラスのメンバーの宣言である場合、関数の仮引数や戻り値の型の宣言である場合は、初期化子は必要ない。



.. code-block:: c++
  
  int obj ;
  
  // クラスの例
  struct S
  {
      int & ref ;
      S() : ref(obj) { }
  } ;
  
  // extern指定子の例
  // このリファレンスは単なる宣言。
  // 実態はどこか別の場所で定義されている
  extern int & external_ref ;
  
  // 関数の仮引数と戻り値の型の例
  int & f( int & ref ) { return ref ; }


リファレンスは必ず、有効なオブジェクトか関数を参照していなければならない。nullリファレンスというものはあり得ない。なぜならば、nullリファレンスを作る方法というのは、nullポインターを参照することである。nullポインターを参照することは、それ自体が未定義動作となるので、規格の上では、合法にnullリファレンスを作ることはできない。



.. code-block:: c++
  
  void f()
  {
      int * ptr = nullptr ;
      int & ref = *ptr ; // エラー、nullポインターを参照している
  }


リファレンスのリファレンスは存在しないということはすでに延べた。ただし、見かけ上、リファレンスが重なるという場合が存在する。



typedef、テンプレート仮引数の型、decltype指定子が、Tへのリファレンス型であるとする。リファレンスというのは単なるリファレンスであり、lvalueリファレンスとrvalueリファレンスの両方を含む。その場合、この型に対するlvalueリファレンスを宣言した場合、Tへのlvalueリファレンスになる。一方、この型に対するrvalueリファレンスを宣言した場合、Tへのリファレンス型になる。



これはどういうことかというと、すでにリファレンス型であるtypedef、テンプレート仮引数、decltype指定子に対して、さらにリファレンスの宣言子を付け加えるという意味である。もし、この型に対して、lvalueリファレンスを宣言しようとした場合、元のリファレンス型の如何に関わらず、lvalueリファレンスとなる。rvalueリファレンスを宣言しようとした場合、元のリファレンス型になる。



.. code-block:: c++
  
  int main()
  {
      typedef int & lvalue_ref ; // lvalueリファレンス
      typedef int && rvalue_ref ; // rvalueリファレンス
  
      // lvalueリファレンスを宣言しようとした場合
      // 元のリファレンス型が、lvalueリファレンスでもrvalueリファレンスでも、lvalueリファレンスになる
      typedef lvalue_ref & type1 ; // int &
      typedef rvalue_ref & type2 ; // int &
  
      // rvalueリファレンスを宣言しようとした場合
      // 元のリファレンス型になる
      typedef lvalue_ref && type3 ; // int &
      typedef rvalue_ref && type4 ; // int &&
  }


換言すれば、lvalueリファレンスは優先され、rvalueリファレンスは無視されるということである。



リファレンスが、内部的にストレージを確保するかどうかは規定されていない。したがって、memcpyなどをつかい、リファレンスを他のストレージの上にコピーすることはできない。




メンバーへのポインター（Pointers to members）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



宣言子が以下のように記述されている場合、メンバーへのポインターを意味する。



.. code-block:: c++
  
  

.. code-block:: c++
  
  struct S
  {
      void func(void) { }
      int value ;
  } ;
  
  void ( S:: * ptr_func )( void ) = &S::func ;
  int S:: * ptr_value = &S::value ;


メンバーへのポインターは、クラスのstaticなメンバーを参照することはできない。また、リファレンス型のメンバーを参照することもできない



.. code-block:: c++
  
  struct S
  {
      static void func(void) { }
      static int value ;
      int & ref ;
  } ;
  int S::value ;
  
  void ( S:: * p1 )( void ) = &S::func ; // エラー
  void ( *p2 ) (void) = &S::func ; // OK
  int S:: * p3 = &S::value ; // エラー


メンバーへのポインターは、ポインターとは異なる型である。staticメンバー関数へのポインターは、メンバー関数ポインターではなく、通常の関数ポインターである。




配列（Arrays）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



宣言子が以下のように記述されている場合、配列を意味する。



.. code-block:: c++
  
  識別子 [ 定

.. code-block:: c++
  
  int a[5] ; // 要素数5のint型の配列
  float b[123] ; // 要素数123のfloat型の配列


型指定子と、配列以前の宣言子を合わせた型を、配列の要素型（element type）という。要素型は、void以外の基本型、ポインター型、メンバーへのポインター型、クラス、enum型、配列型でなければならない。要素型には、リファレンス型、void型、関数型、<a href="#class.abstract">抽象クラス</a>は使えない。



.. code-block:: c++
  
  int a[5] ; // void以外の基本型
  
  int * b[5] ; // ポインター型
  
  struct S { int value ; } ;
  int S::*c[5] ; // メンバーへのポインター型
  
  S d[5] ; // クラス
  
  enum struct E{ value } ;
  E e[5] ; // enum型


配列に対する配列を作ることができる。これを、多次元配列（multidimensional array）という。



.. code-block:: c++
  
  int a[3][5][7] ;


ここでは、aは3 × 5 × 7の配列である。詳しく言うと、aは要素数3の配列である。その各要素は、要素数5の配列である。その各要素は、要素数7のint型の配列である。



配列の定数式は、整数の定数式でなければならない。また、その値は、0より大きくなければならない。



.. code-block:: c++
  
  int a[0] ; // エラー
  int b[-1] ; // エラー


定数式は、配列の要素数を表す。今、定数式の値がNであるとすると、配列の要素数はN個であり、0からN-1までの数字を持って表される。その配列のオブジェクトは、連続したストレージ上に、N個の要素型のサブオブジェクトを持っていることになる。



.. code-block:: c++
  
  int main()
  {
      constexpr int N = 5 ;
      int a[N] ; // 要素数5の配列
      a[0] = 0 ; // 最初要素
      a[4] = 0 ; // 最後の要素
  }


配列の定数式が省略された場合、要素数の不明な配列となる。これは不完全なオブジェクト型である。多次元配列の場合は、最初の配列の定数式のみ省略できる。



定数式の省略された配列は、不完全なオブジェクト型なので、不完全なオブジェクト型の使用が許可されている場所で使うことができる。



.. code-block:: c++
  
  typedef int a[] ; 
  typedef int b[][5][7] ; // 最初の定数式のみ省略可


また、関数の仮引数の型として使うことができる。



.. code-block:: c++
  
  void f( int parameter[] ) { }


ただし、関数の仮引数の場合、型は、要素型への配列ではなく、要素型へのポインターに置き換えられる。詳しくは、宣言子の<a href="#dcl.fct">関数</a>を参照。



宣言に初期化子がある場合、配列の定数式を省略できる。この場合、要素数は、初期化子から決定される。



.. code-block:: c++
  
  int a[] = { 1, 2, 3 } ; // 型はint [3]


詳しくは、初期化子の<a href="#dcl.init.aggr">アグリゲート</a>を参照




関数（Functions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



<p class="editorial-note">
TODO: さらに詳しく説明する可能性あり。



関数の宣言方法
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



関数の宣言子には、文法が二つある。指定子がautoではない場合、以下の文法となる。



.. code-block:: c++
  
  識別子 ( 仮引数リスト ) CV修

この場合、指定子と、指定子に続く識別子以前の宣言子が、戻り値の型になる。



.. code-block:: c++
  
  int f( int ) ; // int型の引数を取り、int型の戻り値を返す関数
  int * f( int, int ) ; // int型の引数とint型の引数を取り、int *型の戻り値を返す関数


この例では指定子のint型は、戻り値の型を意味する。



指定子がautoの場合、以下の文法で関数を宣言できる。



.. code-block:: c++
  
  識別子 ( 仮引数リスト ) CV修

この場合、戻り値の型は、指定子ではなく、宣言子の中に記述される。



.. code-block:: c++
  
  auto f( int ) -> int ; // int型の引数を取り、int型の戻り値を返す関数
  auto f( int, int ) -> int * ; // int型の引数とint型の引数を取り、int *型の戻り値を返す関数


違いは、戻り値の型を指定子で指定するか、宣言子の最後で指定するかである。同じ名前と型の関数は、どちらの文法で宣言されたとしても、同じ関数となる。



.. code-block:: c++
  
  // 関数fの宣言
  int f( int ) ;
  // 同じ関数fの再宣言
  auto f( int ) -> int ;


指定子にautoを書く、新しい関数の宣言子では、戻り値の型を後置できる。この新しい関数の宣言子によって、戻り値の型名の記述に、仮引数名を使うことができる。例えば、今、二つの引数に、operator *を適用する関数を考える。



.. code-block:: c++
  
  template < typename T1, typename T2 >
  ??? multiply( T1 t1, T2 t2 )
  {
      return t1 * t2 ;
  }


ここで、???という部分で、戻り値の型を指定したい。ところが、T1とT2に対してoperator +を適用した結果の型は、テンプレートをインスタンス化するまで分からない。



.. code-block:: c++
  
  struct Mass { } ;
  struct Acceleration { } ;
  struct Force { } ;
  // ニュートンの運動方程式、F=ma
  Force operator *( Mass, Acceleration ) { return Force() ; }
  
  int main()
  {
      Mass m ; Acceleration a ;
      Force f = multiply( m, a ) ;
  }


この例では、Massクラス型とAccelerationクラス型同士をかけ合わせると、結果はForceクラス型となる。すると、関数multiplyの戻り値の型は、式の結果の型でなければならない。一体どうするか。これには、decltypeが使える。decltypeは、式の結果の型を得る指定子である。



.. code-block:: c++
  
  int main()
  {
      Mass m ; Acceleration a ;
      typedef decltype( m * a ) type ; // Force
  }


ところが問題は、従来の関数の文法では、戻り値を記述する場所では、まだ仮引数名が宣言されていないということである。



.. code-block:: c++
  
  template < typename T1, typename T2 >
  decltype( t1 * t2 ) // エラー、t1とt2は宣言されていない
  multiply( T1 t1, T2 t2 )
  {
      return t1 * t2 ;
  }


これを解決するには、やや不自然なメタプログラミングの手法を用いるか、引数を後置できる文法を用いるしかない。新しい関数宣言の文法を用いれば、以下のように書ける。



.. code-block:: c++
  
  template < typename T1, typename T2 >
  auto multiply( T1 t1, T2 t2 ) -> decltype( t1 * t2 )
  {
      return t1 * t2 ;
  }




仮引数リスト
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



仮引数リストは、コンマで区切られた0個以上の仮引数の宣言である。仮引数リストは、関数を呼び出す際に、実引数の型や数を指定する。



.. code-block:: c++
  
  void f( int i, float f, double d, char const * c ) ;


仮引数リストが空である場合、引数を取らないことを意味する。仮引数が(void)の場合は特別なケースで、仮引数リストが空であることと同義である。



.. code-block:: c++
  
  // 引数を取らない関数
  void f( ) ;
  // 同じ意味
  void f( void ) ;


仮引数の名前は省略できる。<a href="#dcl.fct.def">関数の定義</a>に、仮引数の名前が書かれている場合、その名前が仮引数を表す。



.. code-block:: c++
  
  // OK、関数fの宣言、仮引数の名前がない
  void f( int ) ;
  // OK、同じ関数fの宣言、仮引数に名前がある
  void f( int x ) ; 
  
  // OK、同じ関数fの定義
  void f( int x )
  {
      x ; // 仮引数を表す
  }


関数の定義で、仮引数に名前が与えられていない場合、関数の本体から、実引数を使えない。ただし、実引数としては、渡されている。



.. code-block:: c++
  
  void f( int ) { /* 実引数を使えない */ }
  
  int main()
  {
      f( 0 ) ; // 実引数を渡すことには変わりない。
  }


仮引数の名前は、関数の型には影響を及ぼさない。以下はすべて、同じ関数である。型も同じである。オーバーロードではない。



.. code-block:: c++
  
  // 型はvoid (int, int)
  void f( int foo, int bar ) ;
  // 同じ関数fの宣言
  void f( int bar, int foo ) ; 
  
  // 同じ関数fの定義
  void f( int hoge, int /*名前の省略*/ ) { }




関数の型
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



関数の型として意味のあるものは、戻り値の型、仮引数の型リスト、リファレンス修飾子、CV修飾子である。関数の型は、以下のように決定される。



まず、仮引数リストの中のそれぞれの仮引数に対して、指定子と宣言子から、型を決定する。



.. code-block:: c++
  
  // 仮引数リスト：int
  void f( int ) ;
  // 仮引数リスト：int *, int *
  void f( int *, int * ) ;


このようにして得られた仮引数リストの型に対して、以下の変換を行う。



「T型への配列型」は、「T型へのポインター型」に置き換えられる。「関数型」は、「関数ポインター型」に置き換えられる。



.. code-block:: c++
  
  // void ( int * )
  void f( int [3] ) ;
  // void ( int * )
  void g( int [] ) ;
  
  // void ( void (*)(int) )
  void h( void ( int ) ) ;


この変換は、関数の本体の中でも有効である。



.. code-block:: c++
  
  void f( int array[5] )
  {
  // arrayの型は int *である。int [5]ではない
  }
  
  void g( void func( int ) )
  {
  // funcの型は、void (*)(int)である。void (int)ではない
  }


このようにして得られた仮引数の型のリストに対し、さらに変換が行われる。これ以降の変換は、関数の型を決定するための変換であり、関数本体の中の引数の型には影響しない。



トップレベルのCV修飾子を消す。



.. code-block:: c++
  
  // void (int)
  void f( const volatile int ) ;
  // void (int const *)
  void g( int const * const ) ;
  
  // void (int)
  void h( const int x )
  {
  // 関数の本体では、xの型はconst int
  }


関数の本体の中では、引数の型には、トップレベルのCV修飾子も含まれる。しかし、関数の型としては、仮引数に指定されたトップレベルのCV指定子は影響しない。



仮引数の名前がdecltypeに使われている場合、型は、配列からポインター、関数から関数ポインターへの変換が行われた後の型となる。トップレベルのCV修飾子は残る。



.. code-block:: c++
  
  // void ( int *, int * )
  void f( int a[10], decltype(a) b)  ;
  // void ( int, int const * ) ;
  void g( int const a, decltype(a) * b)  ;


仮引数の型に影響を与える<a href="#dcl.stc">ストレージクラス指定子</a>を消す。



.. code-block:: c++
  
  // void (int)
  void f( register int ) ; 


ただし、現行のC++には、仮引数の型に影響を与えるストレージクラス指定子は、registerだけである。registerの使用は推奨されていない。



上記の変換の結果を、仮引数の型リスト（parameter-type-list）という。



関数が非staticなメンバー関数の場合、CV修飾子があるかどうかが、型として考慮される。



.. code-block:: c++
  
  struct S
  {
      // void S::f(void)
      void f() ;
      // void S::f(void) const
      void f() const ;
  } ;


関数が非staticなメンバー関数の場合、リファレンス修飾子があるかどうかが、型として考慮される。



.. code-block:: c++
  
  struct S
  {
      // void S::f(void) &
      void f() & ; 
      // void S::f(void) &&
      void f() && ;
  
      // リファレンス修飾子が省略された関数
      void g() ;
  } ;


メンバー関数に対するCV修飾子とリファレンス修飾子については、<a href="#class.mfct.non-static">非staticメンバー関数</a>を参照。リファレンス修飾子については、<a href="#over.match.funcs">オーバーロード解決の候補関数と実引数リスト</a>も参照。



この他の記述、仮引数名やデフォルト実引数や例外指定は、関数の型には影響しない。



.. code-block:: c++
  
  // void f(int)
  void f( int param = 0 ) noexcept ;


関数の戻り値の型には、関数や配列を使うことはできない。



.. code-block:: c++
  
  // エラー
  auto f() -> void (void);
  auto f() -> int [5] ;


ただし、関数や配列へのポインターやリファレンスは、戻り値の型として使うことができる。



.. code-block:: c++
  
  // OK、ポインター
  auto f() -> void (*)(void);
  auto f() -> int (*)[5] 
  // OK、リファレンス
  auto f() -> void (&)(void);
  auto f() -> int (&)[5]


同じ名前で、型の違う関数を、同じスコープ内で複数宣言して使うことができる。これを、関数のオーバーロードという。詳しくは<a href="#over">オーバーロード</a>項目を参照。






デフォルト実引数（Default arguments）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



仮引数に対して、=に続けて式が書かれていた場合、その式は、デフォルト実引数として用いられる。デフォルト実引数は、関数呼び出しの際に、実引数が省略された場合、かわりに引数として渡される。



.. code-block:: c++
  
  void f( int x = 123, int y = 456 ) { }
  
  int main()
  {
      f( ) ; // f( 123, 456 )と同じ
      f( 0 ) ; // f( 0, 456 )と同じ
      f( 1, 2 ) ; // デフォルト実引数を使用しない
  }


式は、単にリテラルでなくてもよい。



.. code-block:: c++
  
  int f() { return 0 ; }
  void g( int x = f() ) { }


関数の呼び出しの再に、前の実引数を省略して、あとの実引数を指定することはできない。



.. code-block:: c++
  
  void f( int x = 123, int y = 456 ) { }
  int main()
  {
      f( , 0 ) ; // エラー
  }


デフォルト実引数は、関数のパラメーターパックに指定することはできない。



.. code-block:: c++
  
  template < typename ... Types >
  void f( Types .. args = 0 ) ; // エラー


デフォルト実引数は、後から付け加えることも出来る。ただし、再宣言してはいけない。たとえ同じ式であったとしても、再宣言はできない。



.. code-block:: c++
  
  void f( int ) ;
  // OK、デフォルト実引数を付け加える
  void f( int x = 0 ) ;
  // エラー、デフォルト実引数の再宣言
  void f( int x = 0 ) ; 
  // 定義
  void f( int x ) { }


可読性のためには、デフォルト実引数は、関数の最初の宣言に記述すべきである。



.. code-block:: c++
  
  void f( int = 0 ) ; // 宣言
  void f( int ) { } // 定義


デフォルト実引数が使われる場合、式は、関数呼び出しの際に、毎回評価される。評価の順序は規定されていない。




関数の定義（Function definitions）
--------------------------------------------------------------------------------



<p class="editorial-note">
TODO: FDIS後のdefault化とdelete定義の関数の本体への移行に対応すること。



.. code-block:: c++
  
  関数の定義:
      関数の宣言 関数の本体
      関数の宣言 = default ;
      関数の宣言 = delete ;
  
  関数の本体:
      コンストラクター初期

関数の定義とは、関数の宣言に続けて、関数の本体の書かれている関数宣言である。



.. code-block:: c++
  
  void f() ; // 宣言
  void f() {} // 定義
  
  void // 指定子
  g () // 宣言子
  { } // 関数の本体


関数は、名前空間スコープか、クラススコープの中でのみ、定義できる。



.. code-block:: c++
  
  // グローバル名前空間スコープ
  void f() {}
  // クラススコープ
  struct S { void f() {} } ;
  
  void g()
  {
      void h(){} ; // エラー、関数のブロックスコープの中では定義できない
  }


コンストラクター初期化子は、クラスのコンストラクターで用いる。詳しくは、クラスの<a href="#class.ctor">コンストラクター</a>と、クラスの<a href="#class.init">初期化</a>を参照。



関数の定義には、複合文の他に、関数tryブロックを使うこともできる。



.. code-block:: c++
  
  void f()
  try
  {
  // 関数の本体
  }
  catch(...)
  {
  // 例外ハンドラー
  } 


関数tryブロックについて詳しくは、<a href="#except">例外</a>を参照。



関数の本体では、__func__（ダブルアンダースコアであることに注意）という名前の変数が、以下のようにあらかじめ定義されている。



.. code-block:: c++
  
  static const char __func__[] = "関数名" ;


「関数名」とは、実装依存の文字列である。C++規格では、この実装依存の文字列の意味は、何も規定されていない。この機能はC言語から取り入れられたものである。C99規格では、関数本体の属する関数の名前を表す、実装依存の文字列とされている。いずれにせよ、具体的な文字列については、何も規定されていない。




default定義（Explicitly-defaulted functions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  関数の宣言 = default ;


関数の宣言に続けて、= default ;と書く関数の定義を、明示的にデフォルト化された関数（Explicitly-defaulted functions）という。本書では、default定義と呼ぶ。



明示的にデフォルト化された関数は、<a href="#special">特別なメンバー関数</a>でなければならない。また、暗黙的に定義された場合と同等の型でなければならない。デフォルト実引数と例外指定は使えない。



明示的なデフォルト化は、暗黙の定義と同等の定義を、明示的に定義するための機能である。



.. code-block:: c++
  
  struct S
  {
      S() = default ; // default定義
      S(int){ } 
  } ;


この例では、もし、明示的なデフォルト化が書かれていない場合、Sのデフォルトコンストラクターは、暗黙的に定義されない。



明示的にデフォルト化された関数を、暗黙的に定義される関数をあわせて、デフォルト化された関数（defaulted function）という。




delete定義（Deleted definitions）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  関数の宣言 = delete ;


関数の宣言に続けて、= delete ; と書く関数の定義を、削除された定義（Deleted definitions）という。また、本書では、分かりやすさのため、delete定義と呼ぶ。



削除された関数定義は、宣言として存在しているが、定義のない関数である。宣言としては存在しているので、名前解決やオーバーロード解決、テンプレートのインスタンス化の際には、通常通り考慮される。



ただし、削除された関数定義を、宣言以外の方法で参照した場合、エラーとなる。参照というのは、明示的、暗黙的に関数を呼び出すことや、関数へのポインター、メンバーポインター、リファレンスを得ることなどである。また、たとえ未評価式の中であっても、参照した場合エラーとなる。



.. code-block:: c++
  
  // 削除された関数の定義
  void f() = delete ;
  
  void f() ; // OK、宣言はできる
  
  int main()
  {
      f() ; // エラー、削除された関数の呼び出し
      &f ; // エラー、削除された関数のポインターを得ようとしている
      void (& ref )(void) = f ; // エラー、削除された関数のリファレンスを得ようとしている
      typdef decltype(f) type ; // エラー、未評価式の中で、削除された関数を参照している
  }


削除された関数の定義は、関数の最初の宣言でなければならない。



.. code-block:: c++
  
  void f() ; // 削除された定義ではない
  void f() = delete ; // エラー、最初の宣言でなければならない
  
  void g() = delete ; // OK、最初の宣言
  void f() ; // OK、再宣言


ただし、関数テンプレートの特殊化の場合、最初の特殊化の宣言となる。



.. code-block:: c++
  
  template < typename T >
  void f( T ) { } // primary template
  
  // 特殊化
  template < >
  void f<int>(int) = delete ;
  
  int main()
  {
      f(0) ; // エラー
      f(0.0) ; // OK
  }


関数がオーバーロードされている場合、オーバーロード解決によって、削除された関数定義が参照される場合のみ、エラーとなる。



.. code-block:: c++
  
  void f( int ) {} // 削除されていない関数
  void f( double ) = delete ; // 削除された関数定義
  
  int main()
  {
      f( 0 ) ; // OK、void f(int)は削除されていない
      f( 0.0 ) ; // エラー、削除された関数の参照
  }


関数のオーバーロード、関数テンプレート、削除された定義を組み合わせると、非常に面白い事ができる。



.. code-block:: c++
  
  template < typename T >
  void f( T ) { }
  
  // 特殊化でdoubleでインスタンス化された場合の定義を削除
  template < >
  void f<double>(double) = delete ;
  
  void call_f()
  {
  // doubleでインスタンス化した場合、エラーになる
      f( 0 ) ; // OK
      f( true ) ; // OK
      f( 0.0 ) ; // エラー
  }
  
  // あらゆるインスタンス化を削除
  template < typename T >
  void g( T ) = delete ;
  
  // 削除されていない定義
  template < >
  void g< double >( double ) { }
  
  void call_g()
  {
  // double以外でインスタンス化した場合、エラーになる
      g( 0 ) ; // エラー
      g( true ) ; // エラー
      g( 0.0 ) ; // OK   
  }
  
  // 非テンプレートな関数
  void h( int ) { }
  
  // 関数テンプレートの定義を削除
  template < typename T >
  void h( T ) = delete ;
  
  void call_h()
  {
  // intへの標準型変換を禁止
      h( 0 ) ; // OK、非テンプレートな関数を呼び出す
      h( true ) ; // エラー、関数テンプレート
      h( 0.0 ) ; // エラー、関数テンプレート
  }
  
  void i( int ) = delete ;
  void i( double ) { }
  
  void call_i()
  {
  // intからdoubleへの標準変換をエラーにする
      i( 0 ) ; // エラー、
      i( true ) ; // OK
      i( 0.0 ) ; // OK
  }


このように、削除された定義を使うことで、意図しない標準型変換やインスタンス化を阻害できる。



削除された関数定義の具体的な使い方は、実に様々な例が考えられる。ここでは、その一部を挙げる。



クラスのコンストラクターを制御する。



.. code-block:: c++
  
  struct Boolen
  {
      Boolen( ) = delete ;
      Boolen( bool ) { }
  
      template < typename T >
      Boolen( T ) = delete ;
  } ;
  
  int main()
  {
      Boolen a = true ; // OK
      Boolen b = 123 ; // エラー
      Boolen c = &a ; // エラー
  }


Boolenクラスは、必ず、ひとつのbool型の引数で初期化しなければならない。このクラスの初期化の際に、bool以外の型を渡すと、テンプレートのインスタンス化とオーバーロード解決により、関数テンプレート版のコンストラクターが優先される。しかし、定義は削除されているため、エラーとなる。結果的に、暗黙の型変換を禁止しているのと同じ意味となる。そのため、意図しない数値やポインターでの初期化という、つまらないバグを防げる。



クラスのオブジェクトをnewで生成することを禁止する。



.. code-block:: c++
  
  struct Do_not_new
  {
      void *operator new(std::size_t) = delete;
      void *operator new[](std::size_t) = delete;
  } ;
  
  int main()
  {
      Do_not_new a ; // OK
      Do_not_new * ptr = new Do_not_new ; // エラー
      Do_not_new * array_ptr = new Do_not_new[10] ; // エラー
  }


何らかの理由で、あるクラスのオブジェクトを、newで生成してほしくないとする。削除された定義を使えば、あるクラスに対して、newを禁止できる。



クラスのコピーを禁止する。



.. code-block:: c++
  
  struct move_only
  {
      move_only() = default ;
      ~move_only() = default ;
  
      move_only( const move_only & ) = delete ;
      move_only( move_only && ) = default ;
      move_only & operator = ( const move_only & ) = delete ;
      move_only & operator = ( move_only && ) = default ;
  } ;
  
  int main()
  {
      move_only m ;
      move_only n ;
  
      n = m ; // エラー、コピーは禁止されている
      n = std::move(m) ; // OK、ムーブはできる
  }


クラスmove_onlyは、ムーブができるが、コピーはできないクラスになる。




初期化子（Initializers）
--------------------------------------------------------------------------------



宣言子の宣言する変数に対して、初期値を指定することができる。この初期値を指定するための文法を、初期化子（Initializer）という。この初期化子の項目で解説している初期化は、宣言文以外にも、関数の仮引数を実引数で初期化することや、関数の戻り値の初期化、new式やクラスのメンバー初期化子などにも適用される。



初期化子の文法と意味について解説する前に、まず基本的な三つの初期化について解説しなければならない。ゼロ初期化、デフォルト初期化、値初期化である。



ゼロ初期化（zero-initialize）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



ゼロ初期化（zero-initialize）とは、T型のオブジェクトやリファレンスに対して、



Tがスカラー型の場合、整数の定数、0を、T型に変換して初期化する。



.. code-block:: c++
  
  static int x ; // 0で初期化される
  static float f ; // 0がfloat型に変換されて初期化される
  static int * ptr ; // 0がnullポインターに変換されて初期化される


Tがunionではないクラス型の場合、非staticなデータメンバーと基本クラスのサブオブジェクトが、それぞれゼロ初期化される。また、アライメント調整などのための、オブジェクト内のパディングも、ゼロビットで初期化される。



.. code-block:: c++
  
  struct Base { int x ; } ;
  struct Derived : Base
  {
      int y ;
  } ;
  
  // 非staticなデータメンバー、基本クラスのサブオブジェクトが、それぞれゼロ初期化される
  static Derived d ;


この例では、Derivedのデータメンバーであるyと、基本クラスであるBaseのオブジェクトがゼロ初期化される。Baseをゼロ初期化するということは、Baseのデータメンバーであるxもゼロ初期化される。



Tがunion型の場合、オブジェクトの最初の、非staticな名前のつけられているデータメンバーが、ゼロ初期化される。また、アライメント調整などのための、オブジェクト内のパディングも、ゼロビットで初期化される。



.. code-block:: c++
  
  union U
  {
      int x ;
      double d ; 
  } ;


このunionのオブジェクトをゼロ初期化した場合、U::xがゼロ初期化される。



Tが配列型の場合、各要素がそれぞれゼロ初期化される。



Tがリファレンス型の場合、初期化は行われない。




デフォルト初期化（default-initialize）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



デフォルト初期化（default-initialize）とは、T型のオブジェクトに対して、



Tがクラス型の場合、Tのデフォルトコンストラクターが呼ばれる。デフォルトコンストラクターにアクセス出来ない場合は、エラーである。



.. code-block:: c++
  
  class A
  {
  public :
      A() { }
  } ;
  
  class B
  {
  private :
      A() { }
  } ;
  
  int main()
  {
      A a ; // デフォルトコンストラクターが呼ばれる
      B b ; // エラー、デフォルトコンストラクターにアクセスできない
  }


Tが配列型の場合、各要素がそれぞれデフォルト初期化される。



上記以外の場合、初期化は行われない。



.. code-block:: c++
  
  int main()
  {
      int x ; // 初期化は行われない
  }


const修飾された型をデフォルト初期化する場合、型はユーザー定義コンストラクターを持つクラス型でなければならない。



.. code-block:: c++
  
  struct X { } ;
  struct Y { Y() { } } ;
  
  int main ()
  {
      int const a ; // エラー、intはユーザー定義コンストラクターを持つクラス型ではない
      X const b ; // エラー、Xはユーザー定義コンストラクターを持つクラス型ではない
  
      Y const c ; // OK
  }


リファレンス型をデフォルト初期化しようとした場合、エラーになる。





値初期化（value-initialize）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



値初期化（value-initialize）とは、T型のオブジェクトに対して、



Tがクラス型で、ユーザー提供のコンストラクターを持つ場合、Tのデフォルトコンストラクターが呼ばれる。デフォルトコンストラクターにアクセス出来ない場合は、エラーである。



.. code-block:: c++
  
  struct S
  {
      S() { }
      int x ; 
  } ;


クラスSのオブジェクトを値初期化した場合、Sのデフォルトコンストラクターが呼ばれる。xの値は不定である。



Tが、unionではないクラス型で、ユーザー提供のコンストラクターを持たない場合、オブジェクトはゼロ初期化される。もし、暗黙的に定義されたコンストラクターが、トリビアルではない場合、コンストラクターが呼ばれる。



.. code-block:: c++
  
  struct A
  {
      A() {  }
  } ;
  
  struct B
  {
  // ユーザー提供のコンストラクターがない
  // 暗黙に定義されたコンストラクターはトリビアルではない
      A a ;
      int x ;
  } ;


クラスBのオブジェクトを値初期化した場合、Aのデフォルトコンストラクターが呼ばれる。また、xはゼロ初期化される。



Tが配列型の場合、各要素がそれぞれ値初期化される。



上記以外の場合、オブジェクトはゼロ初期化される。



リファレンス型をゼロ初期化しようとした場合、エラーとなる。





staticストレージの期間を持つオブジェクトは、プログラムの開始時に、必ずゼロ初期化される。その後、必要であれば、初期化される。



.. code-block:: c++
  
  struct S
  {
      S() : x(1) { }
      int x ;
  } ;
  
  S s ;// staticストレージの期間を持つオブジェクト


ここでは、Sのデフォルトコンストラクターが実行される前に、データメンバーのxはゼロ初期化されている。



初期化子が空の括弧、()、であるとき、オブジェクトは値初期化される。ただし、通常の宣言文では、初期化子として空の括弧を書く事はできない。なぜならば、空の括弧は、関数の宣言であるとみなされるからだ。



.. code-block:: c++
  
  int main()
  {
      int x() ; // int (void)型の関数xの宣言
  }


初期化子としての空の括弧は、<a href="#expr.new">new</a>、<a href="#expr.type.conv">関数形式の明示的型変換</a>、<a href="#class.base.init">基本クラスとデータメンバーの初期化子</a>で使うことができる。



.. code-block:: c++
  
  struct S
  {
      S()
      : x() // メンバー初期化子
      { }
      int x ;
  }
  
  int main()
  {
      new int() ; // new、初期化子として空の括弧
      int() ; // 関数形式のキャスト
  }


初期化子が指定されていない場合、オブジェクトはデフォルト初期化される。



.. code-block:: c++
  
  struct S { } ;
  
  int main()
  {
      S s ; // デフォルト初期化される
  }


デフォルト初期化では、すでに説明したように、クラス以外の型は、初期化が行われない。初期化が行われないオブジェクトの値は、不定である。



.. code-block:: c++
  
  int main()
  {
      int i ; // 値は不定
      double d ; // 値は不定
  }


ただし、staticやthreadストレージの有効期間を持つオブジェクトは、ゼロ初期化されることが保証されている。



.. code-block:: c++
  
  // グローバル名前空間
  int x ; // staticストレージ、ゼロ初期化される
  thread_local int y ; // threadストレージ、ゼロ初期化される


以下のような文法の初期化子を、コピー初期化（copy-initialization）という。



.. code-block:: c++
  
  T x = a ;


これに加えて、関数の実引数を渡す、関数のreturn文、例外のthrow文、例外を受ける、アグリゲートのメンバーの初期化も、コピー初期化という。この「コピー」という言葉は、コピーコンストラクターやコピー代入演算子とは関係がない。コピー初期化でも、コピーではなく、ムーブされることもある。



以下のような文法の初期化子を、直接初期化（direct-initialization）という。



.. code-block:: c++
  
  T x(a) ;
  T x{a} ;


これに加えて、<a href="#expr.new">new</a>、<a href="#expr.static.cast">static_cast</a>、<a href="#expr.type.conv">関数形式のキャスト</a>、<a href="#class.base.init">基本クラスとデータメンバーの初期化子</a>も、直接初期化という。



初期化子の意味は、以下のように決定される。オブジェクトの型を、目的の型（destination type）とし、初期化子の型を、元の型（source type）とする。元の型は、初期化子が、ひとつの初期化リストか、括弧で囲まれた式リストの場合は、存在しない。



.. code-block:: c++
  
  // 目的の型はT
  // 元の型はint
  T x = 0 ;
  
  // 目的の型はT
  // 元の型は存在しない（ひとつの初期化リスト）
  T x = { } ;
  T x({ }) ;
  T x{ } ;
  
  // 目的の型はT
  // 元の型は存在しない（括弧で囲まれた式リスト）
  T x(1, 2, 3)


初期化子が、ひとつの初期化リストの場合、<a href="#dcl.init.list">リスト初期化</a>される。



.. code-block:: c++
  
  // リスト初期化される
  T x = { } ;
  T x({ }) ;
  T x{ } ;


目的の型がリファレンスの場合、<a href="#dcl.init.ref">リファレンス</a>を参照。



目的の型が、char、signed char、unsigned char、char16_t、char32_t、wchar_tの配列で、初期化子が文字列リテラルの場合、<a href="#dcl.init.string">文字配列</a>を参照。



初期化子が空の()の場合、オブジェクトは値初期化される。



ただし、通常の変数の宣言では、空の()を書く事はできない。なぜならば、空の括弧は、関数の宣言とみなされるからだ。



.. code-block:: c++
  
  // int (void)型の関数xの宣言
  // int x(void) ; と同じ
  int x() ; 


空の()を書く事ができる初期化子には、<a href="#expr.type.conv">関数形式のキャスト</a>、<a href="#expr.new">new</a>、<a href="#class.base.init">メンバー初期化</a>がある。



.. code-block:: c++
  
   // 関数形式のキャスト
  int x = int() ;
  // new
  new int() ;
  
  // メンバー初期化
  class C
  {
      int member ;
      C() : member()
      { }
  } ;


{}や、空の初期化リストを含む({})は、文法上曖昧とならないので、宣言文でも書ける。詳しくは<a href="#dcl.init.list">リスト初期化</a>で解説するが、この場合も、オブジェクトは値初期化される。



.. code-block:: c++
  
  int x{} ; // int型の変数xの宣言と定義と初期化子
  int y({}) ; // int型の変数yの宣言と定義と初期化子


それ以外の場合で、目的の型が配列型の場合、エラーとなる。これは、初期化子がある場合で、上記のいずれにも該当しない場合を指す。



.. code-block:: c++
  
  int a[5] = 0 ; // エラー、int [5]型は、int型で初期化できない


目的の型がクラス型で、初期化子が直接初期化である場合、最も最適なコンストラクターが、オーバーロード解決によって選ばれる。



.. code-block:: c++
  
  struct Elem { } ;
  
  struct S
  {
      S( int ) { }
      S( Elem ) { }
  } ;
  
  int main()
  {
      S s1( 0 ) ; // S::S(int)
      S s2( 0.0 ) ; // S::S(int)、標準型変換による
  
      Elem elem ;
      S s3( elem ) ; // S::S(Elem)
  }


コンストラクターが適用できなかったり、曖昧である場合は、エラーとなる。



.. code-block:: c++
  
  struct S
  {
      S( long ) { }
      S( long long ) { }
  } ;
  
  struct Elem { } ;
  
  int main()
  {
      S s1 ( 0 ) ; // エラー、コンストラクターが曖昧
      Elem elem ;
      S s2( elem ) ; // エラー、適切なコンストラクターが見つからない
  }


目的の型がクラス型で、初期化子がコピー初期化で、初期化子の型が目的の型か、その派生クラス型である場合、直接初期化と同じ方法で初期化される。初期化子の型が目的の型か、その派生クラス型でない場合は、後述。



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  int main()
  {
      Base b1 = Base() ; 
      Base b2 = Derived() ;
  }


目的の型がクラス型で、初期化子がコピー初期化の場合（ただし上記を除く）、ユーザー定義の型変換が試みられ、最適な候補が、オーバーロード解決によって選ばれる。



.. code-block:: c++
  
  struct Elem { } ;
  struct Integer
  {
      operator int () const { return 0 ; }
  } ;
  
  struct S
  {
      S( int ) { }
      S( Elem ) { }
  } ;
  
  int main()
  {
      S s1 = 0 ; // コンストラクターによる変換、S::S(int)
      S s2 = 0.0 ; // 標準型変換の結果、S::S(int)
      S s3 = Elem() ; // コンストラクターによる変換、S::S(Elem)
      S s4 = Integer() ; // Integer::operator int()が呼ばれ、次にS::S(int)
  }


型変換できなかったり、型変換が曖昧である場合は、エラーとなる。



.. code-block:: c++
  
  struct A { } ;
  struct B { } ;
  
  struct C
  {
      C( long ) { }
      C( long long ) { }
  } ;
  
  int main()
  {
      A a ;
      B b = a ; // エラー、変換関数が見つからない
      C c = 0 ; // エラー、変換関数が曖昧
  }


それ以外の場合、つまり、目的の型がクラス型ではない場合で、初期化子の型がクラスであった場合、目的の型に型変換が試みられ、最適な候補がオーバーロード解決によって選択される。型変換ができない場合や、曖昧な場合は、エラーとなる。



.. code-block:: c++
  
  struct S
  {
      operator int() { return 0 ; }
  } ;
  
  int main()
  {
      S s ;
      int x = s ; // OK、S::operator int()が呼ばれる
  }


それ以外の場合、つまり、目的の型も初期化子の型も、クラスではない場合、標準型変換が試みられる。ユーザー定義の変換関数は考慮されない。型変換ができない場合、エラーとなる。



.. code-block:: c++
  
  int main()
  {
      int i = 0 ;
      float f = i ; // OK、整数から浮動小数点数へ型変換される
      int * p = f ; // エラー、floatはint *に変換できない
  }




アグリゲート（Aggregates）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



アグリゲート（aggregate）とは、配列か、いくつかの制約を満たしたクラスである。クラスの場合、ユーザー定義のコンストラクター、非staticデータメンバーの初期化子、privateおよびprotectedな非staticデータメンバー、基本クラス、virtual関数が存在しないものだけを、アグリゲートという。



以下は、アグリゲートの例である。



.. code-block:: c++
  
  struct Aggregate
  {
  // 非staticデータメンバーはすべてpublic
      int x ;
      float y ;
  
  // 非virtualなメンバー関数
      void f() { }
  // staticデータメンバーはpublicでなくてもよい
  private :
      int data ;
  } ;
  int Aggregate::data ;
  
  int a[10] ;
  Aggregate b ;
  Aggregate c[10] ;


以下はアグリゲートの条件を満たさないクラスの例である。



.. code-block:: c++
  
  struct Base { } ;
  
  struct NonAggregate
      : Base // 基本クラス
  {
  // ユーザー定義のコンストラクター
      NonAggregate() { }
  // 非staticデータメンバーの初期化子
      int x = 0 ;
  // privateおよびprotectedな非staticデータメンバー
  private:
      int y ;
  protected ;
      int z ;
  // virtual関数
      virtual void f() { }
  } ;


配列は必ずアグリゲートである。たとえアグリゲートではないクラス型であっても、そのクラスの配列型は、アグリゲートとなる。



.. code-block:: c++
  
  // アグリゲートではないクラス
  struct NonAggregate
  {
      NonAggregate() { }
  } ;
  
  NonAggregate a[3] ; // アグリゲート


アグリゲートが初期化リストで初期化される場合、初期化リストの対応する順番の要素が、それぞれアグリゲートのメンバーの初期化に用いられる。メンバーはコピー初期化される。



.. code-block:: c++
  
  // 配列の例
  int a[3] = { 1, 2, 3 } ;
  // 各要素の初期化、a[0] = 1, a[1] = 2, a[2] = 3
  
  // クラスの例
  struct S
  {
      int x ; int y ;
      double d ;
  } ;
  
  S s = { 1, 2, 3.0 } ;
  // 各メンバーの初期化は、s.x = 1, s.y = 2, s.d = 3.0
  
  // クラスの配列の例
  S sa[3] =
  {
      { 1, 2, 3.0 },
      s, s
  } ;
  
  // アグリゲートではないクラスの配列の例
  class C
  {
      int value ;
  public :
      C(int value) : value(value) { }
  } ;
  
  C obj( 3 ) ; // クラスのオブジェクト
  
  // 配列はアグリゲート
  C ca[3] = { 1, 2, obj } ;
  // コピー初期化を適用した結果、C::C(int)が呼び出される
  // ca[0]は1、ca[1]は2、ca[2]はobjで、それぞれ初期化される


初期化の際に、縮小変換が必要な場合、エラーである。



.. code-block:: c++
  
  int a( 0.0 ) ; // OK
  int b{ 0.0 } ; // エラー、縮小変換が必要
  
  struct S { int x ; } ;
  S s = { 0.0 } ; // エラー、縮小変換が必要


初期化リストが、内部に初期化リストを含む場合、アグリゲートの対応するメンバーは、初期化リストによって初期化される。



.. code-block:: c++
  
  struct Inner { int x ; int y ;  } ;
  struct Outer
  {
      int x ;
      Inner obj ;
  } ;
  
  Outer a = { 1, { 1, 2 } } ;
  // a.x = 1, a.obj = { 1, 2 }
  // a.obj.x = 1, a.obj.y = 2


要素数不定の配列のアグリゲートが、初期化リストで初期化される場合、配列の要素数は、初期化リストの要素数になる。



.. code-block:: c++
  
  int a[] = { 1 } ; // int [1] 
  int b[] = { 1, 2, 3 } ; // int [3]
  int c[] = { 1, 2, 3, 4, 5 } ; // int [5]


staticデータメンバーと無名ビットフィールドは、アグリゲートのリスト初期化の際には、メンバーとして考慮されない。つまり、初期化リストの要素の順番などにも影響しない。



.. code-block:: c++
  
  struct S
  {
      int x ;
      static int static_data_member ;// staticデータメンバー
      int y ;
      int : 8 ; // 無名ビットフィールド
      int z ;
  } ;
  static int S::static_data_member ;
  
  S s = { 1, 2, 3 } ;
  // s.x = 1, s.y = 2, s.z = 3


この例では、static_data_memberと、yとzとの間にある無名ビットフィールドは、リスト初期化の際には、メンバーとして考慮されない。



もし、アグリゲートのメンバーよりも、初期化リストの要素の方が多い場合は、エラーとなる。



.. code-block:: c++
  
  int a[3] = { 1, 2, 3, 4 } ; // エラー
  
  struct S
  {
      int x, int y, int z ;
  } ;
  
  S s = { 1, 2, 3, 4 } ; // エラー


もし、アグリゲートのメンバーよりも、初期化リストの要素の方が少ない場合、明示的に初期化されていないアグリゲートのメンバーは、すべて値初期化される。値初期化では、アグリゲートの条件を満たす型はすべて、ゼロ初期化される。したがって、単にゼロで初期化されると考えても差し支えない。



.. code-block:: c++
  
  int a[5] = { 1, 2, 3 } ;
  // a[0] = 1, a[1] = 2, a[2] = 3
  // a[4]とa[5]は、値初期化される
  
  struct S { int x ; int y ; } ;
  
  S s { 1 } ;
  // s.x = 1
  // s.yは値初期化される


空の初期化リストでは、値初期化される。



.. code-block:: c++
  
  // メンバーはすべて値初期化される
  int a[5] = { } ;
  struct S
  {
      int x ; int y ;
  } ;
  
  S s = { } ;


既存のコードでは、アグリゲートのすべてのメンバーをゼロ初期化するために、{0}という初期化リストが使われていることがある。



.. code-block:: c++
  
  int x[100] = {0} ; // すべてゼロで初期化


これは、C++ではなく、C言語に由来するコードである。C言語では、空の初期化リストを書く事ができない。そのため、Cプログラマは、{0}と書くのである。多くのC++プログラマは、C言語もよく知っているので、既存のコードでは、慣習的に{0}が使われている。しかし、C++では、{0}と書く必要はない。{}で十分である。



アグリゲートが、内部に別のアグリゲートを持っている場合、初期化リストは、その内部のアグリゲートを無視することはできない。



.. code-block:: c++
  
  struct SubAggregate { } ;
  
  struct Aggregate
  {
      int m1 ;
      SubAggregate s1 ;
      int m2 ;
      SubAggregate m2 ;    
      int m3 ;
      SubAggregate m3 ;    
  } ;
  
  SubAggregate s ;
  
  Aggregate a =
  {
      1,
      { },// 空の初期化リスト
      2,
      s,// オブジェクトの変数
      3,
      SubAggregate() // 関数形式のキャスト
  } ;


このように、内部のアグリゲートに続くメンバーを初期化したい場合は、たとえ空の初期化リストでも、必ず書かなければならない。もちろん、その内部のアグリゲートをコピー初期化できる型の値ならば、なんでも使える。



アグリゲート内のリファレンスのメンバーが、明示的に初期化されなかった場合、エラーとなる。



.. code-block:: c++
  
  struct S
  {
      int & ref ; // リファレンスのメンバー
  } ;
  
  int x ;
  S s1 = { x } ; // OK、リファレンスを初期化している
  S s2 = { } ; // エラー、リファレンスが初期化されていない


多次元配列は、初期化リストのネストによって初期化することができる。



.. code-block:: c++
  
  int a[2][2] = { { 1, 2 }, { 1, 2 } } ;
  
  int b[3][3][3] =
  {
      { 1, 2, 3 },
      { 1, 2, 3 },
      { 1, 2, 3 }
  } ;




文字配列（Character arrays）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



char（signed charとunsigned charも含む）, wchar_t, char16_t, char32_tの配列は、それぞれ、対応する文字列リテラルで初期化できる。



.. code-block:: c++
  
  char str[6] = "hello" ;
  char utf8_str[6] = u8"hello" ;
  wchar_t wide_str[6] = L"hello" ;
  char16_t utf16_str[6] = u"hello" ;
  char32_t utf32_str[6] = U"hello" ;


文字列リテラルは、null文字を含むということに注意しなければならない。文字列リテラル、"hello"の型は、char const [6]である。



文字配列の要素数が指定されていない場合、初期化子の文字列リテラルの要素数になる



.. code-block:: c++
  
  // 要素数は6
  char str[] = "hello" ;


配列の要素数より、文字列リテラルの要素数の方が多い場合、エラーとなる。



.. code-block:: c++
  
  char str[5] = "hello" ; // エラー


配列の要素数より、文字列リテラルの要素数の方が少ない場合、明示的に初期化されない要素は、ゼロ初期化される。



.. code-block:: c++
  
  // 以下の二行は同等
  char str[10] = "hello" ;
  char str[10] = { 'h', 'e', 'l', 'l', 'o', '\0', 0, 0, 0, 0 } ;




リファレンス（References）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



<p class="editorial-note">
TODO: FDIS後に見直し。core issue 1058.If the initializer expression is a string literal (2.14.5 [lex.string]), the program is ill-formed.



T &amp;を、「T型へのlvalueリファレンス」という。T &amp;&amp;を、「T型へのrvalueリファレンス」という。これらを二つまとめて、「T型へのリファレンス」という。lvalueリファレンスは、lvalueへのリファレンスであり、lvalueで初期化する。rvalueリファレンスは、rvalueへのリファレンスであり、rvalueで初期化する。そのため、このような名前になっている。



T型へのリファレンスは、T型のオブジェクトか関数、あるいは、T型に変換可能なオブジェクトで初期化できる。



.. code-block:: c++
  
  struct Integer
  {
      int object ;
      operator int & () { return object ; }
  } ;
  
  void f(void) { }
  
  int main()
  {
  // オブジェクトによる初期化
      int int_object ;
      int & ref_int = int_object ;
  
  // 関数による初期化の例
      void ( &ref_function )(void) = f ;
  
  // int型に変換可能なオブジェクトによる初期化
      Integer integer_object ;
      int & ref_integer = integer_object ;
  }


リファレンスは、必ず初期化されなければならない。リファレンスの参照先を変更することはできない。リファレンスは、参照先のオブジェクトと同じように振舞う。



.. code-block:: c++
  
  int main()
  {
      int x ;
      int & ref = x ;
      ref = 0 ; // x = 0 と同じ
      int y = 0 ;
      ref = y ; // x = y と同じ、参照先は変わらない
  }


関数の仮引数、関数の戻り値の型、クラス定義の中のクラスメンバー宣言、extern指定子が明示的に使われている宣言では、リファレンスの初期化子を省略できる。



.. code-block:: c++
  
  // 関数の仮引数
  void f( int & ) ;
  
  // 関数の戻り値の型
  int & g() ;
  auto g() -> int & ;
  
  // クラス定義のクラスメンバーの宣言
  struct S { int & ; } ;
  
  // extern指定子（refは別の場所で定義されている）
  extern int & ref ;


もちろん、これらのリファレンスも、使うときには、初期化されていなければならない。



リファレンスの具体的な初期化について説明する前に、リファレンス互換（reference-compatible）を説明しなければならない。ある型、T1とT2があるとする。もし、T1が、T2と同じ型か、T2の基本クラス型であり、T1のCV修飾子が、T2のCV修飾子と同等か、それ以上の場合、T1はT2に対してリファレンス互換である。



一般に、T1がT2に対してリファレンス互換である場合、T1へのリファレンスは、T2へのリファレンスで初期化できる。



.. code-block:: c++
  
  // AとBとは、お互いにリファレンス互換ではない
  struct A { } ;
  struct B { } ;
  
  A a ;
  B & r1 = a ; // エラー、リファレンス互換ではない
  
  // BaseはDerivedに対して、リファレンス互換である
  // DerivedはBaseに対して、リファレンス互換ではない
  // 基本クラスは派生クラスに対してリファレンス互換であるが、
  // 派生クラスは基本クラスに対してリファレンス互換ではない
  struct Base { } ;
  struct Derived : Base { } ;
  
  Base base ;
  Derived derived ;
  
  Base & r2 = derived ; // OK
  Derived & r3 = base ; // エラー
  
  // Non_const_intはConst_intに対して、リファレンス互換ではない
  // Const_intはNon_const_intに対して、リファレンス互換である
  // CV修飾子が同じか、それ以上である場合、リファレンス互換である
  // CV修飾子が少ない場合、リファレンス互換ではない
  typedef int Non_const_int ;
  typedef int const Const_int ;
  
  Non_const_int nci ;
  Const_int ci ;
  
  Non_const_int & r4 = ci ; // エラー
  Const_int & r5 = nci ; // OK


T型へのlvalueリファレンスは、リファレンス互換なlvalueで初期化できる。



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  int main()
  {
      int object ;
      int & r1 = object ;
  
      Base base ;
      Base & r2 = base ;
  // 派生クラスのlvalueでも初期化できる
      Derived derived ;
      Base & r3 = derived ;
  
      int const const_object ;
      // OK
      int const & r5 = const_object ;
      int const volatile & r6 = const_object;
  }


基本的に、lvalueリファレンスはlvalueでしか初期化できない。xvalueやprvalueで初期化することはできない。また、CV修飾子を取り除くことはできない。以下はエラーの例である。



.. code-block:: c++
  
  #include <utility>
  
  struct A { } ;
  struct B { } ;
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  int main()
  {
  // エラー、BはAに対してリファレンス互換ではない
      A a ;
      B & b = a ; 
  
      int & r1 = 0 ; // エラー、prvalueでは初期化できない
      int x ;
      int & r2 = std::move( x ) ; // エラー、xvalueでは初期化できない
  
      Base base ;
      Derived & r3 = base ; // エラー、派生クラスは基本クラスに対してリファレンス互換ではない
  
      int const ci ;
      int & r4 = ci ; // エラー、CV修飾子が少ないので、リファレンス互換ではない
  } ;


T型へのlvalueリファレンスは、リファレンス互換な型のlvalueに暗黙的に変換できるクラス型のオブジェクトで初期化できる。



.. code-block:: c++
  
  // int &に暗黙的に変換できるクラス
  struct Integer
  {
      int object ;
      operator int & () { return object ; }
  } ;
  
  int main()
  {
      Integer object ;
      int & ref = object ; // OK、暗黙的にリファレンス互換なlvalueに変換できる
  } ;


volatileではない、const T型へのlvalueリファレンスは、rvalueでも初期化できる。rvalueとは、prvalueとxvalueである。



.. code-block:: c++
  
  #include <utility>
  
  int f() { return 0 ; }
  
  int main()
  {
      // OK、prvalueで初期化できる
      int const & r1 = f() ;
      // OK、xvalueで初期化できる
      int object ;
      int const & r2 = std::move( object ) ;
  
      // エラー、たとえconstでも、volatileであってはならない
      int volatile const & r3 = f() ;
  }


volatileではない、const T型へのlvalueリファレンスが、rvalueでも初期化できるというのは、非常に異質なルールである。これは、C++にまだrvalueリファレンスがなかった時代に、リファレンスでrvalueをも参照する必要があったために導入されたルールである。



T型へのrvalueリファレンスは、リファレンス互換なrvalueで初期化できる。rvalueとは、xvalueとprvalueのことである。



.. code-block:: c++
  
  #include <utility>
  
  int f() { return 0 ; }
  
  int main()
  {
      // OK、prvalueで初期化できる
      int && prvalue_ref = f() ;
  
      // OK、xvalueで初期化できる
      int object ;
      int && xvalue_ref = std::move( object ) ;
  }


rvalueリファレンスは、必ずrvalueで初期化しなければならない。lvalueでは初期化できない。



.. code-block:: c++
  
  int object ;
  int && ref = object ; // エラー、lvalueでは初期化できない


rvalueリファレンス自体はlvalueであるということに、注意しなければならない。もし、rvalueリファレンスをrvalueリファレンスで初期化したいのならば、明示的にrvalueにしなければならない。



.. code-block:: c++
  
  #include <utility>
  
  int f() { return 0 ; }
  
  int main()
  {
      int && rvalue_ref = f() ;
      int && r1 = rvalue_ref ; // エラー、rvalue_ref自体はlvalueである。
      int && r2 = std::move( rvalue_ref ) ; // OK、xvalueでの初期化
  }


T型へのrvalueリファレンスは、リファレンス互換な型のrvalueに暗黙的に変換できるクラス型のオブジェクトで初期化できる。



.. code-block:: c++
  
  #include <utility>
  
  // int &&に暗黙的に変換できるクラス
  struct Integer
  {
      int object ;
      operator int && () { return std::move(object) ; }
  } ;
  
  int main()
  {
      Integer object ;
      int && ref = object ; // OK、暗黙的にリファレンス互換なrvalueに変換できる
  }


rvalueリファレンスの初期化子が、リテラルの場合、一時オブジェクトが生成され、参照される。



.. code-block:: c++
  
  int main()
  {
      int && ref = 0 ; // 一時オブジェクトが生成される
  }




リスト初期化（List-initialization）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



リスト初期化（List-initialization）とは、ひとつの{}で囲まれた初期化子を使ってオブジェクトやリファレンスを初期化することである。このような初期化子を、初期化リスト（Initializer list）という。初期化リストの中の、コンマで区切られた式のことを、初期化リストの要素という。



リスト初期化は、直接初期化でも、コピー初期化でも使える。



.. code-block:: c++
  
  T x( { } ) ; // 直接初期化
  T x{ } ; // 直接初期化
  T x = { } ; // コピー初期化


直接初期化のリスト初期化を、直接リスト初期化（direct-list-initialization）といい、コピー初期化のリスト初期化を、コピーリスト初期化（copy-list-initialization）という。



初期化リストの使える場所
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



初期化リストは、以下の場所で使うことができる。



変数定義の初期化子



.. code-block:: c++
  
  T x( { } ) ;
  T x{ } ;
  T x = { } ;


new式の初期化子



.. code-block:: c++
  
  new T{ } ;


return文



.. code-block:: c++
  
  #include <initializer_list>
  
  auto f() -> std::initializer_list<int>
  {
      return { 1, 2, 3 } ;
  }


関数の実引数



.. code-block:: c++
  
  #include <initializer_list>
  
  void f( std::initializer_list<int> ) { }
  
  int main()
  {
      f( { 1, 2, 3 } ) ;
  }


<a href="#expr.sub">添字</a>



.. code-block:: c++
  
  #include <initializer_list>
  
  struct S
  {
      void operator [] ( std::initializer_list<int> ) { }
  } ;
  
  int main()
  {
      S s ;
      s[ { 1, 2, 3 } ] ;
  }


コンストラクター呼び出しの実引数



.. code-block:: c++
  
  #include <initializer_list>
  
  struct S
  {
      S( std::initializer_list<int> ) { }
  } ;
  
  int main()
  {
      S s1( { 1, 2, 3 } ) ;
      S s2{ 1, 2, 3 } ;
      S({ 1, 2, 3 }) ; // 関数形式のキャスト
      S{ 1, 2, 3 } ; // 関数形式のキャスト
  }


非staticデータメンバーの初期化子



.. code-block:: c++
  
  struct S
  {
      int m1[3] = { 1, 2, 3 } ;
      int m2[3]( { 1, 2, 3 } ) ;
      int m3[3]{ 1, 2, 3 } ;
  } ;


メンバー初期化子



.. code-block:: c++
  
  struct S
  {
      int data[3] ;
      // 以下二行は同じ意味
      S() : data{ 1, 2, 3 } { }
      S() : data( { 1, 2, 3 } ) { }
  } ;


代入演算子の右側



.. code-block:: c++
  
  #include <initializer_list>
  
  struct S
  {
      S & operator = ( std::initializer_list<int> ) { }
  } ;
  
  int main()
  {
      S s ;
      s = { 1, 2, 3 } ;
  }




初期化リストによる初期化の詳細
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



初期化リストによる初期化の詳細について説明する前に、縮小変換と、初期化リストコンストラクターを説明する。



縮小変換（narrowing conversion）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



縮小変換（narrowing conversion）とは、暗黙の型変換のうち、変換先の型では、変換元の値を表現できない可能性のある変換のことをいう。具体的には、四種類の変換がある。



浮動小数点数型から整数型への変換。



.. code-block:: c++
  
  // 変換の一例
  int x = double(0.0) ; // 縮小変換、doubleからint


浮動小数点数型の間の変換のうち、long doubleからdoubleかfloatへの変換、doubleからfloatへの変換。



.. code-block:: c++
  
  // 縮小変換の例
  long double ld = 0.0l ;
  double d = ld ; // 縮小変換、long doubleからdouble
  float f = ld ; // 縮小変換、long doubleからfloat
  f = d ; // 縮小変換、doubleからfloat


整数型、もしくはunscoped enum型か、浮動小数点数型への変換。



.. code-block:: c++
  
  // 縮小変換の例
  int i = 0 ;
  double d = i ; // 縮小変換、intからdouble
  enum { e } ;
  d = e ; // 縮小変換、unscoped enumからdouble


ある整数型、もしくはunscoped enum型から、別の整数型かunscoped enum型への変換において、変換先の型が、変換元の型の値を、すべて表現できない場合。



.. code-block:: c++
  
  // short型はint型の値をすべて表現できないとする
  int i = 0 ;
  short s = i ; // 縮小変換


ただし、最初の浮動小数点数型から整数型の変換を除く、三つの変換（浮動小数点間の変換、整数から浮動小数点数への変換、整数型間の変換）には、ひとつ例外がある。もし、変換元が定数式で、その値が変換先の型で表現可能な場合、縮小変換とはみなされない。



.. code-block:: c++
  
  const double cd = 0.0 ; // cdは定数式
  float f = cd ; // 縮小変換ではない
  
  const int ci = 0 ; // ciは定数式
  double d = ci ; // 縮小変換ではない
  short s = ci ; // 縮小変換ではない


これは、ソースコード中に定数式を書いた場合の、煩わしいエラーを防ぐための、例外的なルールである。



この場合、浮動小数点数では、変換元の定数式の値が、変換元の型では、正確に表現できなくてもよい。これは、浮動小数点数の特性に基づくものである。



初期化リストでは、縮小変換は禁止されている。



.. code-block:: c++
  
  int main()
  {
      int a =  0.0 ; // OK
      int b = { 0.0 } ; // エラー、縮小変換
      int c{ 0.0 } ; // エラー、縮小変換
      int d( { 0.0 } ) ; // エラー、縮小変換
  
      // OK、明示的な型変換
      int d{ static_cast<int>(0.0) }  ;
  }




初期化リストコンストラクター（initializer-list constructor）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



ある型をTとして、ひとつのstd::initializer_list&lt;T&gt;を仮引数に取るコンストラクターか、あるいは、最初の仮引数がstd::initializer_list&lt;T&gt;であり、続く仮引数すべてに、デフォルト実引数が指定されている場合、そのコンストラクターを、初期化リストコンストラクター（initializer-list constructor）という。



初期化リストコンストラクターの仮引数の型は、ある型Tに対する、std::initializer_list&lt;T&gt;か、そのリファレンスでなければならない。



.. code-block:: c++
  
  #include<initializer_list>
  
  struct S
  {
      // 初期化リストコンストラクター
      S( std::initializer_list<int> list ) ;
      // リファレンスでもよい
      S( std::initializer_list<int> & list ) ;
      // CV修飾子付きの型に対するリファレンスでもよい
      S( std::initializer_list<int> const & list ) ;
  
      // これも初期化リストコンストラクター
      // デフォルト実引数のため
      S( std::initializer_list<int> list, int value = 0 ) ;
      
      // これらは初期化リストコンストラクターではない
      S( int value = 0, std::initializer_list<int>, short value ) ;
      S( std::initializer_list<int>, short value ) ;
  } ;


初期化リストコンストラクターは、リスト初期化の際に、他のコンストラクターより優先して考慮される。






リスト初期化の方法
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



リスト初期化は、以下のような優先順位で初期化される。先に書いてある条件に一致した場合、その初期化が選ばれ、その条件に対する初期化が行われる。後の条件は、先の条件に一致しなかった場合にのみ、考慮される。最後の条件にも当てはまらない場合は、エラーとなる。



T型のオブジェクト、あるいはT型へのリファレンスに対して――



初期化リストに要素がなく、Tはデフォルトコンストラクターを持つクラス型の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



オブジェクトは値初期化される。



.. code-block:: c++
  
  // デフォルトコンストラクターを持つクラス
  struct A { } ;
  
  int main()
  {
  // すべて、値初期化される
      A a1 = { } ;
      A a2{ } ;
      A a3( { } ) ;
  }




Tがアグリゲートの場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



<a href="#dcl.init.aggr">アグリゲート</a>として初期化される。



.. code-block:: c++
  
  struct Aggregate
  {
      int x ;
      double d ;
      char str[10] ;
  } ;
  // アグリゲートとして初期化
  Aggregate a = { 123, 3.14, "hello" } ;


縮小変換が必要な場合、エラーとなる。



.. code-block:: c++
  
  // エラー、縮小変換が必要。
  int a[1] = { 1.0 } ;


Tがstd::initializer_list<E>の場合
................................................................................

initializer_listのオブジェクトが構築される。この時、initializer_listの各要素は、初期化リストの各要素によって、初期化される。縮小変換が必要な場合は、エラーになる。



.. code-block:: c++
  
  // 空のinitializer_list
  std::initializer_list<int> a = { } ;
  // 要素数3のinitializer_list
  std::initializer_list<int> b = { 1, 2, 3 } ;
  
  // std::stringを要素に持つinitializer_list
  std::initializer_list< std::string > c = { "hello", "C++", "world" } ;
  
  // エラー、縮小変換が必要
  std::initializer_list<int> d = { 0.0 } ;




Tがクラス型の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



適切なコンストラクターが選ばれる。縮小変換が必要な場合は、エラーとなる。まず、初期化リストコンストラクターが優先して選ばれる。



.. code-block:: c++
  
  struct S
  {
      S( std::initializer_list<int> ) { }
      S( std::initializer_list<double> ) { }
  } ;
  
  int main()
  {
      // S::S( std::initializer_list<int> )
      S s1 = { 1, 2, 3 } ;
      S s2{ 1, 2, 3 } ;
      S s3( { 1, 2, 3 } ) ;
  
      // S::S( std::initializer_list<double> )
      S s4 = { 1.0, 2.0, 3.0 } ;
      S s5{ 1.0, 2.0, 3.0 } ;
      S s6( { 1.0, 2.0, 3.0 } ) ;
  }


Tが初期化リストコンストラクターを持たない場合、初期化リストの要素が、実引数リストとみなされ、通常のコンストラクターが、オーバーロード解決によって選ばれる。縮小変換が必要な場合はエラーとなる。



.. code-block:: c++
  
  struct S
  {
      S( int, int ) { }
      S( int, double ) { }
  } ;
  
  int main()
  {
      // S::S( int, int )
      S s1 = { 1, 2 } ;
      // S::S( int, double )
      S s2 = { 1, 2.0 } ;
  
      // エラー、S::S( int, double )が選ばれるが、縮小変換が必要
      S s3 = { 1.0, 2.0 } ;
  }


リスト初期化の優先順位に注意すること。初期化リストが空の場合は、すでに挙げた一番最初のリスト初期化の条件が選ばれ、値初期化されるので、ここでの条件による初期化が行われることはない。初期化リストコンストラクターは、通常のコンストラクターより、常に優先される。



.. code-block:: c++
  
  struct S
  {
      S( std::initializer_list<int> ) { }
      S( double ) { }
  } ;
  
  int main()
  {
      // OK、値初期化される
      S s1 = { } ;
      // エラー、S( std::initializer_list<int> )が選ばれる
      // しかし、縮小変換が必要
      S s2 = { 0.0 } ; 
  }


この例では、s1はリスト初期化の最初の条件である、空の初期化リストを満たすので、値初期化される。s2では、初期化リストコンストラクターが優先される。S::S( double )が考慮されることはない。しかし、この場合、縮小変換が必要なので、エラーとなる。




Tがリファレンス型の場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



正確には、Tがクラス型へのリファレンスか、リファレンス型で、初期化リストが空の場合。



.. code-block:: c++
  
  // 条件に一致する例
  class C { } ;
  
  C && r1 = { } ; // OK、Tがクラス型へのリファレンス
  int && r2 = { } ; // OK、リファレンス型で初期化子が空
  
  // これは条件に一致しない。後の条件を参照
  int && r3 = { 0 } ;


リファレンスされている型に対するprvalueの一時オブジェクトが生成され、初期化リストでリスト初期化される。リファレンスは、その一時オブジェクトを参照する。



.. code-block:: c++
  
  struct A
  {
      int x ;
  } ;
  
  struct B
  {
      B( std::initializer_list<int> ) { }
  } ;
  
  int main()
  {
      A && r1 = { } ;
      A && r2 = { 1 } ;
      B && r3 = { 1, 2, 3 } ;
      int && ref = { } ;
  }


prvalueの一時オブジェクトが生成されることに注意しなければならない。prvalueを参照できるリファレンスは、rvalueリファレンスか、constかつ非volatileなlvalueリファレンスだけである。



.. code-block:: c++
  
  // 以下はOK
  int && r1 = { } ; // OK、rvalueリファレンス
  int const & r2 = { } ; // OK、constかつ非volatileなlvalueリファレンス
  
  // 以下はエラー
  int & r3 = { } ; // エラー、非constなlvalueリファレンス
  int const volatile & r4 = { } ; // エラー、constではあるが、volatileでもある




初期化リストの要素がひとつの場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



オブジェクトは、初期化リストの要素で初期化される。縮小変換が必要な場合はエラーとなる。



.. code-block:: c++
  
  int a{ 0 } ;
  int b( { 0 } ) ;
  int c = { 0 } ;
  
  // 通常のリファレンスの初期化と同じ
  // リファレンスの初期化

初期化リストに要素がない場合
................................................................................

オブジェクトは値初期化される。この条件に当てはまるのは、ポインターがある。クラスは、すでに先の条件に一致しているので、この条件には当てはまらない。



.. code-block:: c++
  
  // pは値初期化される。つまり、nullポインターとなる。
  int * p{ } ;




std::initializer_listの実装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



std::initializer_listがどのように実装されるかは、規格では具体的に規定されていない。ただし、いくつかの保証はある。




std::initializer_list&lt;E&gt;型のオブジェクトは、{}で囲まれた初期化リストによって生成される。このとき、Eの配列が生成され、初期化リストによって初期化される。たとえば、以下のようなコードがあるとき、



.. code-block:: c++
  
  std::initializer_list<int> list = { 1, 2, 3 } ;


以下のように、ユーザー側からは見えない配列が生成される。



.. code-block:: c++
  
  int __array[3] = { 1, 2, 3 } ;
  // 実装依存のstd::initializer_list<int>の初期化の実装例
  // 配列の先頭要素へのポインターと、最後からひとつ後ろのポインターを格納する
  std::initializer_list<int> list( array, array + 3 ) ;


実際には、std::initializer_listには、このようなコンストラクターはない。あくまで参考のための、実装の一例である。



初期化リストにより生成される配列の寿命は、std::initializer_listのオブジェクトの寿命と同じである。



配列は、staticストレージか自動ストレージ上に構築される。動的ストレージの確保が起こることはない。というのも、動的にストレージを確保しなければならない技術的な理由はないからだ。








