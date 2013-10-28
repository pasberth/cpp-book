宣言（Declarations）
================================================================================

単純宣言（simple-declaration）
--------------------------------------------------------------------------------



単純宣言（simple-declaration）は、大きく分けて三つに分割できる。



.. code-block:: c++
  
  アトリビュート指定子 指定子　宣言子 ;


変数や関数の宣言などは、この単純宣言で書かれることになる。



単純宣言のアトリビュート指定子は、宣言子のエンティティに属する。詳しくは、<a href="#dcl.attr">アトリビュート</a>を参照。



指定子というのは、intやclass C、typedefなどを指す。指定子は複数指定できる。



宣言子は、変数や関数、型などを、ひとつする。宣言子も複数指定できる。



.. code-block:: c++
  
  // int型の変数xの宣言
  int // 指定子
  x // 宣言子
  ;
  
  // int const * const型の変数pの宣言
  const int // 指定子
  * const p // 宣言子
  ;
  
  // typeという名前のint型を宣言。
  typedef int // 指定子
  type // 宣言子
  ;


宣言子を複数指定できることには、注意が必要である。例えば、ひとつの宣言文で、複数の変数を宣言することもできる。



.. code-block:: c++
  
  // int型で、それぞれa, b, c, dという名前の変数を宣言
  // 宣言子は4個
  int a, b, c, d ;


これは、比較的分かりやすい。しかし、ポインターや配列、関数などという型は、宣言子で指定するので、ひとつの宣言文で、複数の宣言子を使うということは、非常に読みにくいコードを書く事もできてしまうのである。



.. code-block:: c++
  
  int * a, b, c[5], (*d)(void) ;


この文は非常に分かりにくい。この文を細かく区切って解説すると、以下のようになる。



.. code-block:: c++
  
  int // 指定子
  * a, // int *型の変数
  b, // int型の変数
  c[5], // int [5]型の変数
  (*d)(void) // int(*)(void)型の変数、引数を取らずint型の戻り値を返す関数ポインター
  ;


ひとつの宣言文で複数の宣言子を書くことは避けるべきである。


static_assert宣言（static_assert-declaration）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  static_assert ( 定数式 , 文字列リテラル ) ;


static_assert宣言は、条件付きのコンパイルエラーを引き起こすための宣言である。static_assertの定数式はboolに変換される。結果がtrueならば、何もしない。結果がfalseならば、コンパイルエラーを引き起こす。いわば、コンパイル時のassertとして働くのである。結果がfalseの場合、C++のコンパイラーは文字列リテラルをエラーメッセージとして、何らかの方法で表示する。



.. code-block:: c++
  
  static_assert( true, "" ) ; // コンパイルが通る
  static_assert( false, "" ) ; // コンパイルエラー
  
  // コンパイルエラー
  // 何らかの方法で、helloと表示される。
  static_assert( false, "hello" ) ;


具体的な利用例としては、今、int型のサイズが4バイトであることを前提としたコードを書きたいとする。このコードは当然ながらポータビリティがない。そこで、int型のサイズが4バイトではない環境では、コンパイルエラーになってほしい。これは、以下のように書ける



.. code-block:: c++
  
  static_assert( sizeof(int) == 4, "sizeof(int) must be 4") ;


sizeof(int)が4ではない環境のC++のコンパイラーでは、このコードはコンパイルエラーになる。また、文字列リテラルが、何らかの方法で表示される。



また別の例では、以下のような関数があるとする。



.. code-block:: c++
  
  // 仕様：Derived型はBase型から派生されていること
  template < typename Base, typename Derived >
  void f( Base base, Derived derived )
  {
  // 処理
  }


この関数では、Derivedという型は、Baseという型から派生されていることを前提とした処理を行う。そこで、もしユーザーがうっかり、そのような要求を満たさない型を渡した場合、エラーになって欲しい。これは、以下のように書ける。



.. code-block:: c++
  
  #include <type_traits>
  
  template < typename Base, typename Derived >
  void f( Base base, Derived derived )
  {
      static_assert(
          !std::is_same<Base, Derived>::value // 同じ型でなければtrue
          && std::is_base_of<Base, Derived>::value // DerivedがBaseから派生されていればtrue
          , "Derived must derive Base.") ;
  
  // 処理
  }
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  int main()
  {
      Base b ; Derived d ;
  
      f(b, d) ; // OK
      f(b, b) ; // エラー
  }


このように、テンプレート引数の型が、あらかじめ定められた要求を満たしていない場合、static_assertを使ってコンパイルエラーにすることもできる。



static_assertの文字列リテラルには、<a href="#lex.charset">基本ソース文字セット</a>を使うことができる。C++の実装は、基本ソース文字セット以外の文字を、エラーメッセージとして表示する義務がない。我々日本人としては、日本語を使いたいところだが、すべてのコンパイラーに日本語の文字コードのサポートを義務づけるのが現実的ではない。そのため規格では、現実的に最低限保証できる文字しかサポートを義務づけていない。もちろん、コンパイラーがstatic_assertの日本語表示をサポートするのは自由である。しかし、サポートする義務がない以上、static_assertの文字列リテラルに基本ソース文字セット以外の文字を使うのは、ポータビリティ上の問題がある。



.. code-block:: c++
  
  // 文字列リテラルが表示されるかどうかは実装依存
  static_assert( sizeof(int) == 4, u"このコードはint型のサイズは4であることを前提にしている" ) ;


指定子（Specifiers）
--------------------------------------------------------------------------------



指定子には、ストレージクラス指定子、関数指定子、typedef指定子、friend指定子、constexpr指定子、型指定子がある。



指定子は、組み合わせて使うことができる場合もある。例えば、typedef指定子と型指定子は、組み合わせて使うことができる。その際、指定子の順番には、意味が無い。以下の2行のコードは、全く同じ意味である。



.. code-block:: c++
  
  // int型の別名typeを宣言
  // typedefはtypedef指定子、intは型指定子、typeは宣言子
  typedef int type ;
  int typedef type ;


もちろん、指定子と宣言子は違うので、以下はエラーである。



.. code-block:: c++
  
  // エラー、*は宣言子。宣言子の後に指定子を書く事はできない
  int * typedef type ;


ストレージクラス指定子（Storage class specifiers）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



ストレージクラス指定子には、register、static、thread_local、extern、mutableがある。



ひとつの宣言の中には、ひとつのストレージクラス指定子しか書く事はできない。つまり、ストレージクラス指定子同士は、組み合わせて使うことができない。ただし、thread_localだけは、staticやexternと併用できる。




register指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



register指定子を使ってはならない。registerは、変数への最適化のヒントを示す目的で導入された。これは、まだハードウェアが十分に高速でないので、賢いコンパイラを実装できなかった当時としては、意味のある機能であった。しかし、現在では、ハードウェアの性能の向上により、コンパイラーはより複雑で高機能な実装ができるようになり、registerは単に無視されるものとなってしまった。



registerは歴史的理由により存在する。この機能は、現在では互換性のためだけに残されている機能であり、使用を推奨されていない。また、将来的には廃止されるだろう。




thread_local指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



thread_local指定子のある変数は、<a href="#basic.stc.thread">スレッドストレージの有効期間</a>を持つ。すなわち、thread_localが指定された変数は、スレッドごとに別のオブジェクトを持つことになる。



thread_local指定子は、名前空間スコープかブロックスコープの中の変数と、staticデータメンバーに対して適用することができる。ブロックスコープの変数にthread_localが指定された場合は、たとえstatic指定子が書かれていなくても、暗黙的にstaticと指定されたことになる。



正しい例


.. code-block:: c++
  
  // グローバル名前空間のスコープ
  thread_local int global_variable ;
  
  // 名前の付いている名前空間のスコープ
  namespace perfect_cpp
  {
      thread_local int variable ;
  }
  
  // ブロックスコープ
  void f()
  {
  // 以下の3行は、すべてthread_localかつstaticな変数である。
      thread_local int a ;
      thread_local static int b ;
      static thread_local int c ;
  }
  
  struct C
  {
  // 以下の2行は、すべてthread_localなstaticデータメンバーである。
      static thread_local int a ;
      thread_local static int b ;
  } ;


thread_local指定子は、staticデータメンバーにしか指定できないということには、注意を要する。データメンバーがstaticデータメンバーとなるには、static指定子がなければならない。ブロックスコープ内の変数とは違い、暗黙のうちにstaticが指定されたことにはならない。



.. code-block:: c++
  
  struct C
  {
      // エラー、thread_localは非staticデータメンバーには適用できない。
      thread_local int a ;
  } ;


thread_localが指定された変数に対する、同じ宣言は、すべてthread_local指定されていなければならない。



.. code-block:: c++
  
  // 翻訳単位 1
  thread_local int value ;
  
  // 翻訳単位 2
  extern thread_local int value ;
  
  // 翻訳単位 2
  extern int value ; // エラー、thread_localが指定されていない




static指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



static指定子には、変数をstatic変数にするという機能と、名前を内部リンケージにするという機能がある。static指定子は、変数と関数と無名unionに指定することができる。ただし、ブロックスコープ内の関数宣言と、関数の仮引数に指定することはできない。



.. code-block:: c++
  
  struct C
  {
      // staticデータメンバー
      static int data ;
      // staticメンバー関数
      static void f() {}
  } ;
  
  int main()
  {
      // 変数、static変数になる
      static int x ;
  
      // 無名union、static変数になる
      static union { int i ; float f ; } ;
  }


static指定子が指定された変数は、<a href="#basic.stc.static">静的ストレージの有効期間</a>を持つ。ただし、thread_local指定子も指定されている場合は、<a href="#basic.stc.thread">スレッドストレージの有効期間</a>を持つ。



クラスのメンバーに対するstatic指定子については、<a href="#class.static">staticメンバー</a>を参照。



static指定子とリンケージの関係については、<a href="#basic.link">プログラムとリンケージ</a>を参照。



名前空間スコープにおける、リンケージ指定目的でのstaticの使用は、無名名前空間で代用した方がよい。この機能は、C++11で非推奨にされるはずだったが、直前で見直された。理由は、既存のコードを考えると、この機能を将来的に廃止することはできないからである。



.. code-block:: c++
  
  // グローバル名前空間スコープ
  // 内部リンケージの指定
  static int x ;
  static void f() {} 
  
  // 無名名前空間を使う
  namespace
  {
      static int x ;
      static void f() {} 
  }




extern指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



extern指定子には、名前のリンケージを外部リンケージにするという機能と、名前の定義をしないという機能がある。extern指定子は、変数と関数に適用できる。ただし、クラスのメンバーと関数の仮引数には指定できない。



.. code-block:: c++
  
  // 変数
  extern int i ;
  // 関数
  extern void f() ;


extern指定子と、宣言と定義の関係については、<a href="#basic.def">宣言と定義</a>を参照。


extern指定子とリンケージの関係については、<a href="#basic.link">プログラムとリンケージ</a>を参照。



テンプレートの<a href="#temp.explicit">明示的なインスタンス化</a>と、<a href="#dcl.link">リンケージ指定</a>は、externキーワードを使うが、指定子ではない。




mutable指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



mutable指定子は、constでもstaticでもないクラスのデータメンバーに適用することができる。mutable指定子の機能は、クラスのオブジェクトへのconst指定子を、無視できることである。これにより、constなメンバー関数から、データメンバーを変更することができる。



.. code-block:: c++
  
  class C
  {
  private:
      mutable int value ;
  
  public :
      void f() const
      {
          // 変更できる
          value = 0 ;
      }
  } ;
  
  int main()
  {
      C c ;
      c.f() ;
  }


mutableの機能について詳しくは、<a href="#dcl.type.cv">CV修飾子</a>も参照。






関数指定子（Function specifiers）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数指定子（Function specifier）には、inline、virtual、explicitがある。



inline指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



inline指定子が書かれた関数宣言は、インライン関数（inline function）を宣言する。inline指定子は、この関数をインライン展開することが望ましいと示すための機能である。ただし、インライン関数だからといって、必ずしもインライン展開されるわけではない。インライン関数ではなくても、インライン展開されることもある。あくまで最適化のヒントに過ぎない。



.. code-block:: c++
  
  // インライン関数
  inline void f() { }


クラス定義の中の関数定義は、inline指定子がなくても、自動的にinline関数になる。



.. code-block:: c++
  
  struct C
  {
      // 関数定義、インライン関数である
      void f() {}
      // 関数の宣言、インライン関数である
      inline void g() ;
      // 関数の宣言、インライン関数ではない
      void h() ;
  } ;
  
  // 関数C::gの定義
  inline void C::g() { }
  
  // 関数C::hの定義
  void C::h() { }


インライン指定子は、関数のリンケージに何の影響も与えない。インライン関数のリンケージは、通常の関数と同じである。すなわち、static指定子があれば内部リンケージ持つ。そうでなければ外部リンケージを持つ。



.. code-block:: c++
  
  // 外部リンケージを持つ
  inline void f() {}
  // 内部リンケージを持つ
  inline static void g() {}


ただし、インライン関数は、外部リンケージを持っていたとしても、通常の関数とは異なる扱いを受ける。これは、インライン展開の実装を容易にするための制約である。インライン関数は、その関数を使用するすべての翻訳単位で、「定義」されていなければならない。インライン関数の定義は、すべての翻訳単位で、まったく同一でなければならない。



.. code-block:: c++
  
  // 翻訳単位 1
  // translation_unit_1.cpp
  
  // 外部リンケージを持つインライン関数の定義
  inline void f() {}
  inline void g() {}


.. code-block:: c++
  
  // 翻訳単位 2
  // translation_unit_2.cpp
  
  // 宣言だけ
  inline void f() ;
  
  // 定義
  inline void g() {}
  
  // 関数の宣言
  int main()
  {
      // エラー
      // この翻訳単位に関数fの定義がない
      f() ; 
  
      // OK、定義もある
      g() ;
  }


これは、テンプレートと同じような制限となっている。そのため、外部リンケージを持つインライン関数は、通常、ヘッダーファイルに書き、必要な翻訳単位で#includeする。まったく同一ということに関して、詳しくは、<a href="#basic.def.odr">ODR（One definition rule）</a>を参照。



ただし、翻訳単位に定義があればいいので、呼び出す場所では、宣言だけだとしても、問題はない。



.. code-block:: c++
  
  // 宣言
  inline void f() ;
  
  int main()
  {
      // すでに名前fは宣言されていて、この翻訳単位に定義がある
      f() ; // OK
  }
  
  // 定義
  inline void f() {} 




virtual指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



virtual指定子は、クラスの非staticメンバー関数に指定することができる。詳しくは、<a href="#class.virtual">virtual関数</a>を参照。




explicit指定子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



explicit指定子は、クラス定義内のコンストラクターと変換関数に指定することができる。詳しくは、<a href="#class.conv.ctor">コンストラクターによる型変換</a>と、<a href="#class.conv.fct">変換関数（Conversion functions）</a>を参照。






typedef指定子（The typedef specifier）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



typedef指定子は、型の別名を宣言するための指定子である。この別名のことを、typedef名（typedef-name）という。typedef名は、型と同じように扱われる。



.. code-block:: c++
  
  typedef int integer ;
  // これ以降、typedef名integerは、int型とおなじように使える。
  
  integer main()
  {
      integer x = 0 ;
      integer y = x ;
  }


typedef名は、エイリアス宣言（alias-declaration）で宣言することもできる。



.. code-block:: c++
  
  using 識別子 = 型名 ;


.. code-block:: c++
  
  using integer = int ;


エイリアス宣言では、usingキーワードに続く識別子が、typedef名となる。typedef指定子によって宣言されたtypedef名と、エイリアス宣言によって宣言されたtypedef名は、全く同じ意味を持つ。そのため、本書で「typedef名」と記述されている場合、それはtypedef指定子による宣言であろうと、エイリアス宣言による宣言であろうと、等しく適用される。一方、「typedef指定子」と記述されている場合、エイリアス宣言には当てはまらない。



エイリアス宣言の文法は、typedefより分かりやすい。例えば、関数ポインターの別名を宣言したいとする。



.. code-block:: c++
  
  // 同じ意味
  typedef void (*type)(void) ;
  using type = void (*)(void) ;


typedef指定子は、指定子であるので、単純宣言と同じ文法で名前を宣言しなければならない。using宣言は、名前を先に書き、その後に、純粋な型名を書くことができる。



エイリアス宣言とテンプレートについては、<a href="#temp.alias">テンプレートエイリアス</a>を参照。




<p class="editorial-note">
TODO: この部分、規格の文面に問題あり。


typedef指定子は、クラス以外の同じスコープ内で、同じ型のtypedef名を再宣言することができる。



.. code-block:: c++
  
  typedef int I ;
  typedef int I ; // OK、同じ型の再宣言
  typedef short I ; // エラー、型が違う
  
  void f()
  {
      typedef short I ; // OK、別のスコープなので別の宣言
  }
  
  struct Class_Scope
  {
      typedef int type ;
      typedef int type ; // エラー、クラススコープ内では、同じ型でも再宣言できない
  } ;


typedef名とconstの関係は、一見して分かりにくい。



.. code-block:: c++
  
  typedef int * type ;
  
  // aの型はint const *
  const int * a ; 
  // bの型は、int * const 
  const type b ; 


これは、指定子と宣言子との違いによる。



.. code-block:: c++
  
  const int // 指定子
  * a // 宣言子
  ;
  
  const type // 指定子、typeの型は int *
  b // 宣言子
  ;


変数aの場合、const intへのポインター型となる。変数bの場合、const type型となる。typeの型は、int *なので、int *へのconst型となる。そのため、違う型となる。




friend指定子（The friend specifier）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



friend指定子については、<a href="#class.friend">friend</a>を参照




constexpr指定子（The constexpr specifier）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



constexpr指定子は、constexprの制約を満たした、変数の定義、関数と関数テンプレートの宣言、staticデータメンバーの宣言に対して指定できる。



.. code-block:: c++
  
  constexpr int value = 0 ;


constexpr指定子を使って定義され、定数式で初期化された変数は、定数式として使うことができる。



.. code-block:: c++
  
  void f()
  {
      constexpr std::size_t size = 10 ;
      int a[size] ;
  }


constexpr指定子を使う変数の型は、リテラル型でなければならない。



.. code-block:: c++
  
  struct literal
  {
      int a ;
  } ;
  
  struct non_literal
  {
      non_literal() { }
  } ;
  
  int main()
  {
      constexpr literal a{} ; // OK
      constexpr non_literal b{} ; // エラー
  }


コンストラクター以外の関数にconstexpr指定子を記述すると、その関数は、constexpr関数(constexpr function)となる。コンストラクターにconstexpr指定子を記述すると、そのコンストラクターは、constexprコンストラクター(constexpr constructor)となる。constexpr関数とconstexprコンストラクターは暗黙にinlineになる。



constexpr関数の定義は、以下の条件を満たさなければならない。



* 
virtual関数でないこと

* 
戻り値の型がリテラル型であること

* 
仮引数の型がリテラル型であること

* 
  
関数の本体は、= deleteか、= defaultか、複合文であること。



  
複合文として使える文は、以下のものだけである。



  *   
null文

  *   
static_assert宣言

  *   
typedef宣言とエイリアス宣言で、クラスやenumを定義しないもの

  *   
using宣言

  *   
usingディレクティブ

  *   
return文ひとつ




* 
戻り値を初期化する際のコンストラクター呼び出しや、暗黙の型変換は、すべて定数式でなければならない。



以下は合法なconstexpr関数の例である。



.. code-block:: c++
  
  constexpr int f()
  {
      return 1 + 1 ;
  }
  
  constexpr int g( int x, int y )
  {
      return x + y + f() ;
  }
  
  constexpr int h( unsigned int n )
  {
      return n == 0 ? 0 : h( n - 11 ) ;
  }


以下は、constexpr関数の制約を満たさない誤ったコードの例である


.. code-block:: c++
  
  // エラー、使えない文の使用
  constexpr int f( )
  {
      constexpr int x = 0 ;
      return x ;
  }
  
  // エラー、使えない文の使用
  constexpr int g( bool b )
  {
      if ( b )
          return 1 ;
      else
          return 2 ;
  }
  
  // エラー、return文がふたつ
  constexpr int h()
  {
      return 0 ;
      return 0 ;
  }
  
  // エラー、戻り値の型がリテラル型ではない
  struct S{ S(){ } } ;
  constexpr S i()
  {
      return S() ;
  }


C++11のconstexpr関数の制約はとても厳しい。C++14では、この制約は大幅に緩和される。



constexprコンストラクターの定義は、仮引数の型がリテラルでなければならない。関数の本体は、= deleteか、= defaultか、複合文でなければならない。複合文は以下の制約を満たさなければならない。



* 
クラスはvirtual基本クラスを持たないこと

* 
関数の本体は関数tryブロックではないこと

* 
  
関数の本体の複合文は、以下のいずれかしか含まないこと



  *   
null文

  *   
static_assert宣言

  *   
typedef宣言とエイリアス宣言で、クラスやenumを定義しないもの

  *   
using宣言

  *   
usingディレクティブ




* 
クラスの非staticデータメンバーと、基本クラスのサブオブジェクトは、すべて初期化されること

* 
非staticデータメンバーと基本クラスのサブオブジェクトの初期化に関わるコンストラクターは、constexprコンストラクターであること

* 
  
非staticデータメンバーに指定された初期化句は定数式であること



  .. code-block:: c++  
    
    struct S
    {
        int member = 0 ; // 定数式であること
    
        constexpr S() { }
    } ;
  


* 
コンストラクターの実引数を仮引数の型に変換する際の型変換は、定数式であること



constexprコンストラクターは、ユーザー定義の初期化を記述したリテラル型のクラスを書くことができる。



.. code-block:: c++
  
  struct point
  {
      int x ;
      int y ;
  
      constexpr S( int x, int y )
          : x(x), y(y)
      { }
  } ;


このようなリテラル型のクラスは、constexpr指定子を使った変数で使える。



.. code-block:: c++
  
  constexpr S s( 10, 10 ) ;


どのような実引数（無引数関数も含む）を与えても、constexprが定数式にならない場合、エラーとなる。



.. code-block:: c++
  
  // OK、定数式になる実引数がある
  constexpr int f( bool b )
  {
      return b ? throw 0 : 0 ;
  }
  
  // エラー、絶対に定数式にならない。
  constexpr int g( )
  {
      throw ;
  }


constexpr関数テンプレートや、クラステンプレートのconstexprメンバー関数のインスタンス化された特殊化が、constexpr関数の制約を満たさない場合、そのような関数やコンストラクターは、constexpr関数、constexprコンストラクターとはみなされない。



.. code-block:: c++
  
  template < typename T >
  constexpr T f( T x )
  {
      return x ;
  }
  
  struct non_literal { non_literal(){ } } ;
  
  int main()
  {
      f( 0 ) ; // OK、constexpr関数
  
      non_literal n ;
      f( n ) ; // OK、ただし通常の関数
  }


constexpr関数を呼び出した結果の値は、同等だがconstexprではない関数を呼び出した結果の値と等しくなる。



コンストラクターを除く非staticメンバー関数にconstexpr指定子を使うと、そのメンバー関数はconst修飾される。



.. code-block:: c++
  
  struct S
  {
      constexpr int f() ; // constになる
  } ;


これは、以下のように書くのと同等である。



.. code-block:: c++
  
  constexpr int f() const ;


constexpr指定子は、これ以外には関数の型に影響を与えない。



constexpr非staticメンバー関数を持つクラスは、リテラル型でなければならない。



.. code-block:: c++
  
  // OK、リテラル型
  struct literal
  {
      constexpr int f() { return 0 ; }
  } ;
  
  // エラー、リテラル型ではない
  struct non_literal
  {
      non_literal() { }
      constexpr int f() { return 0 ; }   
  } ;


constexpr指定子が変数定義に使われた場合、変数はconstになる。変数の型はリテラル型でなければならず、また初期化されなければならない。



.. code-block:: c++
  
  constexpr int a = 0 ;
  
  // エラー、初期化されていない
  constexpr int b ;
  
  
  struct non_literal { non_literal() { } } ;
  // エラー、リテラル型ではない
  constexpr non_literal c{ } ;


初期化にコンストラクター呼び出しが行われる場合、コンストラクター呼び出しは定数式でなければならない






型指定子（Type specifiers）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



型指定子（type specifier）には、クラス指定子、enum指定子、単純型指定子（simple-type-specifier）、複雑型指定子（elaborated-type-specifier）、typename指定子、CV修飾子（cv-qualifier）がある。



クラス指定子は<a href="#class">クラス</a>で、enum指定子は<a href="#dcl.enum">enumの宣言</a>で、typename指定子は、テンプレートの<a href="#temp.res">名前解決</a>を参照。



型指定子は、一部を除いて、宣言の中にひとつだけ書くことができる。組み合わせることのできる型指定子は、以下の通りである。



constは、const以外の型指定子と組み合わせることができる。volatileは、volatile以外の型指定子と組み合わせることができる。



signedとunsignedは、char, short, int, longを後に書くことができる。



shortとlongは、intを後に書くことができる。



longは、doubleを後に書くことができる。longは、longを後に書くことができる。



.. code-block:: c++
  
  long double a = 0.0l ;
  long long int b = 0 ;


CV修飾子（The cv-qualifiers）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



CV修飾子（cv-qualifier）は、指定子の他に、ポインターの宣言子にも使うことができる。CV修飾子には、constとvolatileがある。この二つのキーワードの頭文字をとって、CV修飾子と呼ばれている。CV修飾子付きの変数は、必ず初期化子が必要である。CV修飾子がオブジェクトに与える影響については、基本事項の<a href="#basic.type.qualifier">CV修飾子</a>を参照。



.. code-block:: c++
  
  const int a = 0 ;
  volatile int b = 0 ;
  const volatile int c = 0 ;
  
  const int d ; // エラー、初期化子がない


指定子の始めに延べたように、指定子の順番に意味はないので、const intとint constは、同じ意味となる。



CV修飾子付きの型へのポインターやリファレンスは、必ずしも、CV修飾子付きのオブジェクトを参照する必要はない。ただし、CV修飾子が付いているように振舞う。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ; // 非constなオブジェクト
      x = 0 ; // 変更できる
  
      int const & ref = x ; // 参照する
      ref = 0 ; // エラー、変更できない
  }




単純型指定子（Simple type specifiers）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



単純型指定子には、基本型、クラス名、enum名、typedef名、auto指定子、decltype指定子を使うことができる。



基本型については、<a href="#basic.fundamental">基本型</a>を参照。



注意すべきこととしては、signedやunsignedは、単体で使われると、int型だとみなされる。



.. code-block:: c++
  
  // signed int
  signed a = 0 ;
  // unsigned int
  unsigned b = 0 ;


また、shortやlongやlong longは、それぞれintが省略されたものとみなされる



.. code-block:: c++
  
  // short int
  short a = 0 ;
  // long int
  long b = 0 ;
  // long long int
  long long c = 0 ;




複雑型指定子（Elaborated type specifiers）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



複雑型指定子の複雑（Elaborated）というのは、あまりふさわしい訳語ではないが、本書では便宜上、elaboratedに対し、複雑という訳語を使用する。class、struct、union、enumなどのキーワードを使った型指定子を指す。



.. code-block:: c++
  
  struct StructName { } ;
  class ClassName { } ;
  union UnionName { } ;
  enum struct EnumName { value } ;
  
  int main()
  {
      {
          // 複雑型指定子
          struct StructName a ;
          class ClassName b ;
          union UnionName c ;
          enum EnumName d = EnumName::value ;
      }
  
      {
          // 単純型指定子
          StructName a ;
          ClassName b ;
          UnionName c ;
          EnumName d = EnumName::value ;
      }
  }


識別子に対するキーワードは、enumにはenumキーワードを、unionにはunionキーワードを、クラスにはstructキーワードかclassキーワードを、すでに行われた宣言と一致して使わなければならない。



.. code-block:: c++
  
  class Name { } ;
  struct Name a ; // OK、structキーワードでもよい
  
  enum Name b ; // エラー、キーワードが不一致
  union Name c ; // エラー、キーワードが不一致




auto指定子（auto specifier）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ここでは、変数の宣言に対するauto指定子について説明する。関数の宣言に対するauto指定子については、宣言子の<a href="#dcl.fct">関数</a>を参照。また、<a href="#expr.new">new式</a>にも、似たような機能がある。



変数を宣言する際、型指定子にautoキーワードを書くと、変数の型が、初期化子の式から推定される。



.. code-block:: c++
  
  auto a = 0 ; // int
  auto b = 0l ; // long
  auto c = 0.0 ; // double
  auto d = 0.0l ; // long double


もちろん、単なるリテラルだけにはとどまらない。およそ初期化子に書ける式ならば、何でも使うことができる。



.. code-block:: c++
  
  int f() { return 0 ; }
  
  bool g(int){ return true ; }
  char g(double){ return 'a' ; }
  
  int main()
  {
      auto a = f() ; // int
  
      // もちろん、オーバーロード解決もされる
      auto b = g(0) ; // bool
      auto c = g(0.0) ; // char
  
      auto d = &f ; // int (*)(void)
  }


auto指定子は、冗長な変数の型の指定を省くためにある。というのも、初期化子の型は、コンパイル時に決定できるので、わざわざ変数の型を指定するのは、冗長だからだ。また、変数の型を指定するのが、非常に面倒な場合もある。



.. code-block:: c++
  
  #include <vector>
  #include <string>
  
  int main()
  {
      std::vector< std::string > v ;
      // 型名が長くて面倒
      std::vector< std::string >::iterator iter1 = v.begin() ;
  
      // 簡潔に書ける
      auto iter2 = v.begin() ;
  }


この場合では、std::vector&lt; std::string &gt;::iterator型の変数を宣言している。auto指定子を使わないと、非常に冗長になってしまう。



.. code-block:: c++
  
  template < typename T1, typename T2 > struct Add { } ;
  template < typename T1, typename T2 > struct Sub { } ;
  
  template < typename T1, typename T2 >
  Add< T1, T2 > operator + ( T1, T2 )
  {
      typedef Add< T1, T2 > type ;
      return type() ;    
  }
  
  template < typename T1, typename T2 >
  Sub< T1, T2 > operator - ( T1, T2 )
  {
      typedef Sub< T1, T2 > type ;
      return type() ;    
  }
  
  struct A { } ;
  struct B { } ;
  
  int main()
  {
      A a ; B b ;
      auto result = a + b - b + (b - a) ;
  }


この場合、resultの型を明示的に書こうとすると、以下のようになる。これはとてもではないが、まともに書く事はできない。



.. code-block:: c++
  
  Add< Sub< Add< A, B>, B>, Sub< B, A> > result = a + b - b + (b - a) ;


auto指定子による変数の宣言では、変数の型は、関数のテンプレート実引数の推定と同じ方法で推定される。



.. code-block:: c++
  
  auto u = expr ;


という式があったとすると、変数uの型は、



.. code-block:: c++
  
  template < typename U > void f( U u ) ;


このような関数を、f(expr)と呼び出した場合の、テンプレート仮引数Uと同じ型となる。



ただし、auto指定子では、初期化子が初期化リストであっても、型を推定できるという違いがある。



.. code-block:: c++
  
  // std::initializer_list<int>
  auto a = { 1, 2, 3 } ;
  // std::initializer_list<double>
  auto b = { 1.0, 2.0, 3.0 } ;
  
  // エラー、型を推定できない
  auto c = { 1, 2.0 } ;
  auto d = { } ;
  
  // OK、明示的なキャスト
  auto e = std::initializer_list<int>{ 1, 2.0 } ;
  auto f = std::initializer_list<int>{ } ;


テンプレートの実引数推定と同じ方法で型を推定するために、配列型は配列の要素へのポインターに、関数型は関数ポインタ―型になってしまう。これには注意が必要である。



.. code-block:: c++
  
  void f() { }
  
  int main()
  {
      int a[1] ;
      auto t1 = a ; // int *
      auto t2 = f ; // int (*)(void)
  }


auto指定子は、他の指定子や、CV修飾子、宣言子と組み合わせることもできる。



.. code-block:: c++
  
  int const expr = 0 ; // exprの型はint const
  auto a = expr ; // int
  auto const b = expr ; // int const
  auto const & c = expr ; // int const &
  auto const * d = &expr ; // int const *
  
  static auto e = expr ; // static指定子付きのint型の変数


この際の型の決定も、関数のテンプレート実引数の推定と同じルールになる。



宣言子と初期化子の型が合わない場合は、エラーとなる。



.. code-block:: c++
  
  auto & x = 0 ; // エラー


この例では、xの型は、リファレンス型であるが、初期化子の型は、リファレンス型ではない。そのため、エラーとなる。



宣言子がrvalueリファレンスの場合、注意を要する。auto指定子の型は、テンプレート実引数の推定と同じ方法で決定されるので、lvalueリファレンスになることもある。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      int && r1 = x ; // エラー、rvalueリファレンスをlvalueで初期化できない
  
      auto && r2 = x ; // OK、ただし、r2の型はint &
      auto && r3 = std::move(x) ; // OK、r3の型はint &&
  }


これは、テンプレート実引数の推定と同じである。



.. code-block:: c++
  
  template < typename U >
  void f( U && u ) { }
  
  int main()
  {
      int x = 0 ;
  
      f( x ) ; // Uはint &
      f( std::move(x) ) ; // Uはint &&
  }


auto指定子で変数を宣言する場合は、必ず初期化子がなければならない。また、宣言しようとしている変数名が、初期化子の中で使われていてはならない。



.. code-block:: c++
  
  auto a ; // エラー、初期化子がない
  auto b = b ; // エラー、初期化子の中で宣言しようとしている変数名が使われている


初期化子が要素の型Uの初期化リストの場合、autoの型はstd::initializer_list&lt;U&gt;になる。



.. code-block:: c++
  
  // std::initializer_list<int>
  auto a = { 1, 2, 3 } ;


宣言子が関数の場合、auto指定子を使った宣言は関数になる。



.. code-block:: c++
  
  void f() { }
  auto (*p)() -> void = &f ;


auto指定子を使って、ひとつの宣言文で複数の変数を宣言することは可能である。その場合、変数の型は、それぞれの宣言子と初期化子から推定される型になる。



.. code-block:: c++
  
  auto a = 0, & b = a, * c = &a ;


この例では、aの型はint、bの型はint &amp;、cの型はint *となる。ただし一般に、コードの可読性の問題から、ひとつの宣言文で複数の変数を宣言するのは、避けたほうがよい。



ただし、複数の変数を宣言する場合、autoによって推定される型は、必ず同じでなければならない。



.. code-block:: c++
  
  int x = 0 ;
  auto a = x, * b = &x ; // OK、autoに対して推定される型は同じ
  auto c = 0, d = 0.0 ; // エラー、型が同じではない


従来の、変数が自動ストレージの有効期間を持つということを明示的に指定する意味でのauto指定子は、廃止された。C++11では、autoキーワードを昔の文法で使用した場合、エラーとなる。



.. code-block:: c++
  
  auto int x = 0 ; // エラー、C++11には存在しない昔の機能




decltype指定子（decltype specifier）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  decltype ( 式 )


decltypeの型は、オペランドの式の型になる。decltype指定子のオペランドの式は、未評価式である。



.. code-block:: c++
  
  int main()
  {
      decltype( 0 ) x ; // xの型はint
      decltype( x ) y ; // yの型はint
  
      int const c = 0 ;
      decltype( c ) z = 0 ; // zの型はint const
  }


decltype指定子の型は、以下のような順序で、条件の合うところで、上から優先的に決定される。



decltype(e)に対して、



もし、eが括弧式で囲まれていない、名前かクラスのメンバーアクセスであれば、decltypeの型は、名前eの型になる。



.. code-block:: c++
  
  int x ;
  // decltype(x)の型はint
  decltype(x) t1 ;
  
  class C { int value ; } ;
  C c ;
  // decltype(c)の型は、class C
  decltype(c) t2 ;
  // decltype(c.value)の型は、int
  decltype(c.value) t3 ;


もし、eが関数呼び出しかオーバーロード演算子の呼び出しであれば、decltypeの型は、関数の戻り値の型になる。この際、括弧式は無視される。eという名前が見つからない場合や、eの名前がオーバーロード関数のセットであった場合、エラーとなる。



decltypeのオペランドは未評価式なので、sizeofなどと同じく、関数が実際に呼ばれることはない。



.. code-block:: c++
  
  int f() ;
  
  // decltype( f() )の型は、int
  decltype( f() ) t1 ;
  // decltype( (f()) )の型は、int
  decltype( (f()) ) t2 ;
  
  // エラー、fooという名前は見つからない
  decltype( foo ) t3 ;
  
  // エラー、オーバーロード関数のセット
  void f(int) ;
  void f(short) ;
  
  decltype(f) * ptr ;


もし、eがxvalueであれば、eの型をTとした場合、decltype(e)の型は、T &amp;&amp;となる。



.. code-block:: c++
  
  int x ;
  // typeの型はint &&
  using type = decltype( static_cast< int && >(x) ) ;


もし、eがlvalueであれば、eの型をTとした場合、decltype(e)の型は、T &amp;となる。



.. code-block:: c++
  
  int x ;
  // decltype( (x) ) の型は、int &
  using type = decltype ( (x) ) ;


上記以外の場合、decltypeの型は、eの型となる。



.. code-block:: c++
  
  // decltype(0)の型は、int
  decltype(0) t1 ;
  // delctype("hello")の型は、char const [6]
  decltype("hello") t2 = "hello" ;


eがlvalueで、しかも括弧式で囲まれている場合は、リファレンス型になるということには、注意を要する。



.. code-block:: c++
  
  int x = 0 ;
  
  decltype ( x ) t1 = x ; // t1の型はint
  decltype( (x) ) t2 = x ; // t2の型はint &


decltypeは、他の型指定子や宣言子と併用できる。



.. code-block:: c++
  
  int x ;
  decltype ( x ) * ptr ; // int *
  decltype ( x ) const & const_ref ; // int const &


decltypeは、ネストされた名前の指定子として使用できる。



.. code-block:: c++
  
  struct C
  {
      typedef int type ;
  } ;
  
  int main()
  {
      C c ;
      decltype(c)::type x = 0 ; // int
  }


decltypeは、基本クラスの指定子、メンバー初期化子として、として使用できる。



.. code-block:: c++
  
  struct Base { } ;
  Base base ;
  
  struct Derived
      : decltype(base) // decltypeを基本クラスとして指定
  {
      Derived ()
          : decltype(base) () // メンバー初期化子
      { }
  } ;


decltypeは、疑似デストラクター名として使用できる。



.. code-block:: c++
  
  struct C { } ;
  
  int main()
  {
      C c ;
      c.~decltype(c)() ; // 疑似デストラクターの呼び出し
  }






enumの宣言（Enumeration declarations）
--------------------------------------------------------------------------------



enum指定子は、名前付きの定数と型を宣言、定義する。enum（Enumeration）は、歴史的に列挙型と呼ばれている。enum型の名前は、enum名といい、enumが宣言する定数のことを、列挙子（enumerator）と呼ぶ。



.. code-block:: c++
  
  // Eはenum名、valueは列挙子
  enum E { value = 0 } ;


本書では、enumの機能を四種類に大別して解説する。unscoped enum、scoped enum、enum基底（enum-base）、enum宣言（opaque-enum-declaration）である。



unscoped enum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  enum指定子:
      enum 識

enumというキーワードだけで宣言するenumのことを、unscoped enumという。unscoped enumは、弱い型付けのenumを宣言、定義する。enumの定義は、それぞれ別の型を持つ。列挙子リストとは、コンマで区切られた識別子である。各列挙子には、=に続けて定数を指定することで、値を指定できる。これをenumの初期化子という。ただし、列挙子自体はオブジェクトではない。enumは先頭の列挙子に初期化子がない場合、値は0になる。先頭以外の列挙子に初期化子がない場合、そのひとつ前の列挙子の値に、1を加算した値になる。



.. code-block:: c++
  
  // a = 0, b = 1, c = 2
  enum E { a, b, c } ;
  
  // a = 3, b = 4, c = 5
  enum E { a = 3, b = 4 , c = 5 } ;
  
  // a = -5, b = -4, c = -3
  enum E { a = -5, b, c } ;
  
  // a = 0, b = 1, c = 0, d = 1
  enum E { a, b, c = 0, d } ;


宣言した列挙子は、次の列挙子から使うことができる。



.. code-block:: c++
  
  // a = 0, b = 0, c = 5, d = 3
  enum E { a, b = a, c = a + 5, d = c - 2 } ;


enum名とunscoped enumの列挙子は、enum指定子があるスコープで宣言される。



.. code-block:: c++
  
  enum GlobalEnum { a, b } ;
  
  GlobalEnum e1 = a ;
  GlobalEnum e2 = b ;
  
  int main()
  {
      enum LocalEnum { c, d } ;
      GlobalEnum e1 = c ;
      GlobalEnum e2 = d ;
  }


unscoped enumによって宣言された列挙子は、整数のプロモーションによって、暗黙的に整数型に変換できる。整数型は、明示的なキャストによって、enum型に変換できる。整数型の値が、enum型の表現できる範囲を超えていた場合の挙動は、未定義である。



.. code-block:: c++
  
  enum E { value = 123 } ;
  
  void f()
  {
      int x = value ; // enum Eからintへの暗黙の型変換
  
      E e1 = 123 ; // エラー、intからenum Eへの暗黙の型変換はできない
      E e2 = static_cast<E>(123) ; // intからenum Eへの明示的なキャスト
  }
  
  // コマンドの種類を表す定数
  enum Command { copy, cut, paste } ;
  
  // コマンドを処理する関数
  void process_command( Command id )
  {
      switch( id )
      {
          case copy :
              // 処理
              break ;
          case cut :
              // 処理
              break ;
          case paste :
              // 処理
              break ;
  
          default :
              // エラー処理
              break ;
      }
  }


クラスのスコープ内で宣言された列挙子の名前は、クラスのメンバーアクセス演算子（::, ., -&gt;）を使うことによって、参照することができる。



.. code-block:: c++
  
  struct C
  {
      enum { value } ;
      // クラススコープのなかでは名前のまま参照できる
      void f() { value ; }
  } ;
  
  int main()
  {
      C::value ; // ::による参照
      C c ;
      c.value ; // .による参照
      C * p = &c ;
      p->value ; // ->による参照
  }


unscoped enumは、識別子を省略することができる。



.. code-block:: c++
  
  // 識別子あり
  enum E { a } ;
  
  // 識別子なし
  enum { b } ;




scoped enum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



scoped enumは、強い型付けをするenumである。



.. code-block:: c++
  
  enum struct 識別子 enum

scoped enumは、enum structかenum classという連続した二つのキーワードによって宣言する。enum structとenum classは、全く同じ意味である。どちらを使ってもよい。enumには、クラスのようなアクセス指定はない。scoped enumの識別子は省略できない。列挙子リストの文法は、unscoped enumと変わらない。



.. code-block:: c++
  
  enum struct scoped_enum_1 { a, b, c } ;
  enum classs scoped_enum_2 { a, b, c } ;


scoped enumは、非常に強い型付けを持っている。列挙子は、scoped enumが宣言されているスコープに導入されることはない。かならず、enum名に::演算子をつけて参照しなければならない。



.. code-block:: c++
  
  enum struct E { value } ;
  
  value ; // エラー、scoped enumの列挙子は、このように参照できない
  E::value ; // OK


このため、同じスコープ内で、同じ名前の列挙子を持つ、複数のscoped enumを宣言することもできる。



.. code-block:: c++
  
  void f()
  {
      // scoped enumの場合
      enum struct Foo { value } ;
      enum struct Bar { value } ; // OK
  
      Foo::value ; // enum struct Fooのvalue
      Bar::value ; // enum struct Barのvalue
  }
  
  void g()
  {
      // unscoped enumの場合
      enum Foo { value } ;
      enum Bar { value } ; // エラー、すでにvalueは宣言されている。
  }


scoped enumの列挙子は、暗黙的に整数型に変換することはできない。明示的にキャストすることはできる。整数型からenumへの変換は、unscoped enumと変わらない。つまり、明示的なキャストが必要である。



.. code-block:: c++
  
  enum struct E { value = 123 } ;
  
  int x = E::value ; // エラー、scoped enumの列挙子は暗黙的に変換できない
  int y = static_cast<int>( E::value ) ; // OK、明示的なキャスト
  
  E e = static_cast<E>( 123 ) ; // OK、unscoped enumと同じ


ただし、switch文の中のcaseラベルや、非型テンプレート実引数では、scoped enumも使うことができる。



.. code-block:: c++
  
  enum struct E { value } ;
  template < int N > struct C { } ;
  
  void f( E e )
  {
      // switch文のcaseラベル
      switch( e )
      { case E::value : ; }
  
      // 非型テンプレート実引数
      C< E::value > c ;
  }


これが許されている理由は、scoped enumの内部的な値は使わないものの、強い型付けがされた一種のユニークな識別子として、scoped enumを使えるようにするためである。



scoped enumは、強い型付けをするenumである。scoped enumは、列挙子の内部的な値は使わないが、単に名前付きの状態を表すことができる変数が欲しい場合。また、たとえ内部的な値を使うにしても、強い型付けによって、些細なバグを未然に防ぎたい場合などに使うことができる。




enum基底（enum-base）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  enum基底:
      : 型指定子


enum型は、内部的には単なる整数型である。この内部的な整数型のことを、内部型（underlying type）という。enum基底（enum-base）は、この内部型を指定するための文法である。enum基底の型は、基本クラスの指定とよく似た文法で指定することができる。enum基底の型指定子は、整数型でなければならない。



enum基底が指定されたenum型の内部型は、enum基底の型指定子の型になる。



.. code-block:: c++
  
  enum E : int { } ; // 内部型はint
  
  enum struct Foo : int { } ; // 内部型はint
  enum struct Bar : unsigned int { } ; // 内部型はunsigned int
  
  enum Error : float { } ; // エラー、enum基底が整数型ではない


enum基底が省略された場合、scoped enumの内部型は、intになる。



.. code-block:: c++
  
  enum struct E { } ; // scoped enumのデフォルトの内部型はint


scoped enumで、int型の範囲を超える値の列挙子を使いたい場合は、明示的にenum基底を指定しなければならない。



unscoped enumのenum基底が省略された場合、内部型は明確に定められることがない。



.. code-block:: c++
  
  enum E { } ; // 内部型は定められない。


enumの内部型が定められていない場合、内部型は、enumの列挙子をすべて表現できる整数型になる。その際、どの整数型が使われるかは、実装依存である。どの整数型でも、すべての列挙子を表現できない場合は、エラーとなる。




enum宣言（opaque-enum-declaration）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



enum宣言は、正式には、opaque-enum-declarationという。これは、定義をしないenumの宣言である。関数や変数が、定義せずに宣言できるように、enumも、定義せずに宣言することができる。



.. code-block:: c++
  
  enum 識別子 enum基底 ;
  enum struct 識別子 enum

unscoped enumの場合は、必ず定義と一致するenum基底を指定しなければならない。scoped enumの場合は、enum基底を省略した場合、内部型はデフォルトのintになる。ただし、安全のためには、enum宣言と対応するenumの定義には、enum基底を明示的に書いておいたほうがよい。



.. code-block:: c++
  
  enum struct Foo : unsigned int ; // 内部型はunsigned int
  enum class Bar ; // enum基底が省略された場合、内部型はint
  
  enum E1 : int ; // 内部型はint
  
  enum E2 ; // エラー、unscoped enumの宣言では、enum基底を省略してはならない。


enum宣言によって、宣言のみされたenum名は、通常のenumと同じように使用できる。ただし、列挙子を使うことはできない。なぜならば、列挙子は宣言されていないからだ。



列挙子を使うことができないenum宣言に、何の意味があるのか。enum宣言が導入された背景には、ある種の利用方法では、すべての翻訳単位に列挙子が必要ないこともあるのだ



無駄な定義を省く
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. code-block:: c++
  
  // 翻訳単位 1
  
  enum ID : int { /* 自動的に生成される多数の列挙子 */ } ;


.. code-block:: c++
  
  // 翻訳単位 2
  
  enum ID : int ; // enum宣言
  void f( ID id ) // IDを引数にとる関数
  {
      int x = id ;
      id = static_cast<ID>(0) ;
  }


翻訳単位 1で定義されているenumの列挙子は、外部のツールによって、自動的に生成されるものだとしよう。この定義は、かなり頻繁に更新される。もし、翻訳単位 2では、enumの内部的な値が使われ、列挙子という名前付きの定数には、それほど意味が無い場合、この自動的に生成される多数の列挙子は、無駄である。なぜならば、enumが生成されるたびに、たとえ翻訳単位 2のソースコードに変更がなく、再コンパイルが必要ない場合でも、わざわざコンパイルしなおさなければならないからだ。



なぜenumの定義が必要かというと、完全な定義がなければ、enumの内部型を決定できないからである。C++11では、enum基底によって、明示的に内部型を指定できる。これにより、enumを定義せず宣言することができるようになった。




型安全なデータの秘匿
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

以下のクラスを考える。



.. code-block:: c++
  
  // クラスCのヘッダーファイル
  // C.h
  enum struct ID { /* 自動的に生成される多数の列挙子 */ } ;
  
  class C
  {
  public :
      // 外部に公開するメンバー
  
  private :
      ID id ;
  } ;


さて、このクラスを、複数の翻訳単位で使いたいとする。このクラスには、データメンバーとしてenum型の変数があるが、これは外部に公開しない。クラスの中の実装の都合上のデータメンバーである。enumの列挙子は、外部ツールで自動的に生成されるものとする。



すると、このヘッダーファイルを#includeしているソースファイルは、enumが自動的に生成されるたびに、再コンパイルしなければならない。しかし、このクラスを使うにあたって、enumの定義は必要ないはずである。この場合にも、enum宣言が役に立つ。



.. code-block:: c++
  
  // クラスCのヘッダーファイル
  // C.h
  
  enum struct ID : int ;
  
  class C { /* メンバー */ } ;


.. code-block:: c++
  
  // クラスCのソースコード
  // C.cpp
  
  enum struct ID : int  { /* 自動的に生成される多数の列挙子 */ } ;
  
  // メンバーの実装


このようにしておけば、enumの定義が変更されても、クラスのヘッダーファイルを#includeして、クラスを使うだけのソースコードまで、再コンパイルする必要はなくなる。
</p>]




名前空間（Namespaces）
--------------------------------------------------------------------------------



名前空間とは、宣言の集まりに名前をつける機能である。名前空間の名前は、::演算子によって、宣言を参照するために使うことができる。名前空間は、複数定義することができる。グローバルスコープも、一種の名前空間スコープとして扱われる。



名前空間の定義（Namespace definition）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  inli

名前空間は、別の名前空間スコープの中か、グローバルスコープに書くことができる。名前空間の本体には、あらゆる宣言を、いくつでも書くことができる。これには、名前空間自身も含まれる。



.. code-block:: c++
  
  // グローバルスコープ
  
  namespace NS
  { // NSという名前の名前空間のスコープ
      // 宣言の例
      int value = 0 ;
      void f() { }
      class C { } ;
      typedef int type ;
  }// NSのスコープ、ここまで 
  
  int main()
  {
      // NS名前空間の中の名前を使う
      NS::value = 0 ;
      NS::f() ;
      NS::C c ; 
      NS::type t ;
  
      value ; // エラー、名前が見つからない
  }


名前空間は、名前の衝突を防ぐために使うことができる。



.. code-block:: c++
  
  // グローバルスコープ
  int value ;
  int value ; // エラー、valueという名前はすでに宣言されている
  
  // OK、名前空間Aのvalue
  namespace A { int value ; }
  // OK、名前空間Bのvalue
  namespace B { int value ; }
  
  int main()
  {
      value ; // グローバルスコープのvalue
      A::value ; // 名前空間Aのvalue
      B::value ; // 名前空間Bのvalue
  }


グローバル変数として、valueような、分かりやすくて誰でも使いたがる名前を使うのは、問題が多い。しかし、名前付きの名前空間スコープの中であれば、名前の衝突を恐れずに、気軽に短くて美しい名前でも使うことができる。



名前空間は、何度でも定義することができる。



.. code-block:: c++
  
  // 最初の定義
  namespace NS { int x ; }
  
  // 二度目の定義
  namespace NS { int y ; }


名前空間はネストできる。



.. code-block:: c++
  
  namespace A { namespace B { namespace C { int value ; } } }
  
  int main()
  {
      A::B::C::value ; // Aの中の、Bの中の、Cの中のvalue
  }


inline名前空間
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



inlineキーワードの書かれた名前空間の定義は、inline名前空間である。inline名前空間スコープの中で宣言された名前は、inline名前空間の外側の名前空間のスコープの中でも使うことができる。



.. code-block:: c++
  
  inline namespace NS { int value ; }
  
  namespace Outer
  {
      inline namespace Inner
      {
          int value ;
      } 
  }
  
  int main()
  {
      value ; // NS::value
      NS::value ;
  
      Outer::value ; // Outer::Inner::value
      Outer::Inner::value ;
  }




無名名前空間（Unnamed namespaces）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



TODO:変更されそうなので保留




名前空間のメンバーの定義（Namespace member definitions）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ある名前空間スコープの中で宣言された名前を、その名前空間のメンバーと呼ぶ。名前空間のメンバーは、名前空間の外側で定義することができる。



.. code-block:: c++
  
  namespace NS
  {
      void f() ; // 関数fの宣言
      namespace Inner
      {
          void g() ; // 関数gの宣言
          void h() ; // 関数hの宣言
      }
      void Inner::g() { } // 関数gの定義
  }
  
  void NS::f() { } // 関数fの定義
  void NS::Inner::h() { } // 関数hの定義


ただし、名前空間の外側で定義されているからといって、名前空間の外側のスコープにも、名前が導入されるわけではない。あくまで、名前空間の外側でも、定義ができるだけである。






名前空間エイリアス（Namespace alias）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  namespace 識別子 = 名前空間の名前 ;


名前空間エイリアス（Namespace alias）とは、名前空間の名前の別名を定義する機能である。



名前空間は、名前の衝突を防いでくれる。しかし、名前空間の名前自体が衝突してしまうこともある。それを防ぐためには、名前空間の名前には、十分にユニークな名前をつけなければならない。しかし、衝突しない名前をつけようとすると、どうしても、短い名前をつけることはできなくなってしまう。



.. code-block:: c++
  
  namespace Perfect_cpp
  {
      int x ;
  }
  
  int main()
  {
     Perfect_cpp::x = 0 ;
  }


この例では、十分にユニークな名前、Perfect_cppを使っている。このため、xという名前の変数名でも、衝突を恐れず使うことができる。しかし、このPerfect_cppは長い上に、大文字とアンダースコアを使っており、タイプしづらい。そこで、名前空間エイリアスを使うと、別名を付けることができる。



.. code-block:: c++
  
  namespace Perfect_cpp { int x ; }
  
  int main()
  {
      namespace p = Perfect_cpp ;
      p::x ; // Perfect_cpp::x
  }


ネストされた名前にも、短い別名をつけることができる。



.. code-block:: c++
  
  namespace Perfect_cpp { namespace Library { int x ; } }
  
  int main()
  {
      namespace pl = Perfect_cpp::Library ;
      pl::x ; // Perfect_cpp::Library::x
  }


別名の別名を定義することもできる。



.. code-block:: c++
  
  namespace Long_name_is_Looooong { }
  namespace long_name = Long_name_is_Looooong ;
  namespace ln = long_name ;


同じ宣言領域で、別名と名前空間の名前が衝突してはならない



.. code-block:: c++
  
  namespace A { } namespace B { }
  
  // エラー、同じ宣言領域では、別名と名前空間の名前が衝突してはならない
  namespace A = B ;
  
  int main()
  {
      // OK、別の宣言領域なら可
      namespace A = B ;
  }




using宣言（The using declaration）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  using 識別子 ;


using宣言は、宣言が書かれている宣言領域に、指定した名前を導入する。これにより、明示的に名前空間名と::演算子を使わなくても、その宣言領域で、名前が使えるようになる。



using宣言を、名前空間のメンバーに使う場合、using宣言が書かれているスコープで、::演算子による明示的なスコープの指定なしに、その名前を使うことができる。



.. code-block:: c++
  
  namespace NS { int name ; }
  
  int main()
  {
      name = 0 ; // エラー、名前nameは宣言されていない
  
      using NS::name ;
      name = 0 ; // NS::nameと解釈される
      NS::name = 0 ; // 明示的なスコープの指定
  }
  
  // ブロックスコープ外でもusing宣言は使える
  using NS::name ;


using宣言は、テンプレート識別子を指定することはできない。テンプレート名は指定できる。



.. code-block:: c++
  
  namespace NS
  {
      template < typename T > class C { } ;
  }
  
  int main()
  {
      using NS::C ; // OK、テンプレート名は指定できる
      using NS::C<int> ; // エラー、テンプレート識別子は指定できない
  }


using宣言は、名前空間の名前を指定することはできない。



.. code-block:: c++
  
  namespace NS { }
  using NS ; // エラー


using宣言は、scoped enumの列挙子を指定することはできない.



.. code-block:: c++
  
  namespace NS
  {
      enum struct E { scoped } ;
      enum { unscoped } ;
  }
  
  int main()
  {
      using NS::unscoped ; // OK、unscoped enumの列挙子
      using NS::E::scoped ; // エラー、scoped enumの列挙子は指定できない
  }


using宣言は、その名の通り、宣言である。したがって、通常通り、外側のスコープの名前を隠すこともできる。<a href="#namespace.udir">usingディレクティブ</a>とは、違いがある。



.. code-block:: c++
  
  int name  ; // グローバルスコープのname
  namespace NS { int name ; } // NS名前空間のname
  
  int main()
  {
      // ここではまだ、名前が隠されてはいない
      name = 0 ; // ::nameを意味する
  
      using NS::name ; // このusing宣言は::nameを隠す
      name = 0 ; // NS::nameを意味する
  }


using宣言は、宣言された時点で、すでに宣言されている名前を、スコープに導入する。宣言場所から見えない名前は、導入されない。



.. code-block:: c++
  
  namespace NS { void f( int ) { } }
  // void NS::f(int)をグローバルスコープに導入する
  // void NS::f(double)は、この時点では宣言されていないので、導入されない
  using NS::f ; 
  namespace NS { void f( double ) { } }
  
  int main()
  {
      // この時点で、unqualified名fとして名前探索されるのは
      // void NS::f(int)のみ
      f( 1.23 ) ; // NS::f(int)を呼ぶ。
  
      using NS::f ; // void NS::f(double) をmain関数のブロックスコープに導入する
      f( 1.23 ) ; // オーバーロード解決により、NS::f(double)を呼ぶ
  }


ただし、テンプレートの部分的特殊化は、プライマリークラステンプレートを経由して探すので、たとえusing宣言の後に宣言されていたとしても、発見される。



.. code-block:: c++
  
  namespace NS
  {
      template < typename T >
      class C { } ;
  }
  
  using NS::C ;
  
  namespace NS
  {
      template < typename T >
      class C<T * > { } ; // ポインター型への部分的特殊化
  }
  
  int main()
  {
      C<int * > c ; // 部分的特殊化が使われる。
  }


using宣言は、<a href="#class.inhctor">コンストラクターの継承</a>に使うこともできる。詳しくは、該当の項目を参照。ここでは、クラスのメンバー宣言としてusing宣言を使う際の、文法上の注意事項だけを説明する。



クラスのメンバー宣言としてusing宣言を使う場合、基本クラスのメンバー名を指定しなければならない。名前空間のメンバーは指定できない。using宣言は、基本クラスのメンバー名を、派生クラスのスコープに導入する。



.. code-block:: c++
  
  namespace NS { int value ; }
  
  class Base
  {
  public :
      void f() { } 
  } ;
  
  class Derived : private Base
  {
  public :
      using Base::f ; // OK、基本クラスのメンバー名
      using NS::value ; // エラー、基本クラスのメンバーではない
  } ;


クラスのメンバー宣言としてのusing宣言は、基本クラスのメンバーの名前を、クラスのメンバーの名前探索で発見させることができる。



.. code-block:: c++
  
  struct Base { void f( int ) { } } ;
  struct Derived1 : Base
  {
      void f( double ) { }
  } ;
  struct Derived2 : Base
  {
      using Base::f ;
      void f( double ) { }
  } ;
  
  int main()
  {
      Derived1 d1 ;
      d1.f( 0 ) ; // Derived::f(double)を呼ぶ
      Derived2 d2 ;
      d2.f( 0 ) ; // Base::f(int)を呼ぶ
  }


Derived1::fは、Base::fを隠してしまうので、Base::fはオーバーロード解決の候補関数に上がることはない。Derived2では、using宣言を使って、Base::fをDerived2のスコープに導入しているので、オーバーロード解決の候補関数として考慮される。



また、using宣言は、基本クラスのメンバーのアクセス指定を変更する目的でも使える。



.. code-block:: c++
  
  class Base
  {
      int value ;
  public :
      int get() const { return value ; }
      void set( int value ) { this->value = value ; }
  } ;
  
  // Baseからprivateで派生
  class Derived : private Base
  {
  public : // Base::getのみpublicにする
      using Base::get ;
  } ;


この例では、DerivedはBaseからprivate派生している。ただし、Base::getだけは、publicにしたい。そのような場合に、using宣言が使える。



using宣言でクラスのメンバー名を指定する場合、クラスのメンバー宣言でなければならない。クラスのメンバー宣言以外の場所で、using宣言にクラスのメンバー名を指定してはならない。



.. code-block:: c++
  
  struct C
  {
      int x ;
      static int value ;
  } ;
  
  int C::value ;
  
  using C::x ; // エラー、これはクラスのメンバー宣言ではない
  using C::value ; // エラー、同上




usingディレクティブ（Using directive）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  using namespace 名前空間名 ;


usingディレクティブ（using directive）は、その記述以降のスコープにおける非修飾名前探索に、指定された名前空間内のメンバーを追加するための指示文である。usingディレクティブを使うと、指定された名前空間内のメンバーを、::演算子を用いないで使用できる。



.. code-block:: c++
  
  namespace NS
  {
      int a ;
      void f() { }
      class C { } ;
  }
  
  int main()
  {
      using namespace NS ;
  
      a = 0 ; // NS::a
      f() ; // NS::f
      C c ; // NS::C
  }


usingディレクティブを使えば、指定された名前空間内のすべてのメンバーを、明示的な::演算子を使わずにアクセスできるようになる。



usingディレクティブは、名前空間スコープとブロックスコープ内で使用することができる。クラススコープ内では使用できない。



.. code-block:: c++
  
  namespace A { typedef int type ; }
  
  void f()
  {
      // ブロックスコープ内
      using namespace A ;
      type x ; // A::type
  }
  
  namespace B
  {
      // 名前空間スコープ
      using namespace A ;
      type x ; // A::type
  }
  
  other_namespace::type g1 ; // A::type
  
  // 名前空間スコープ（グローバルスコープ）
  using namespace A ;
  type g2 ; // A::type
  
  class C
  {
      using namespace A ; // エラー、クラススコープ内では使用できない
  } ;


グローバルスコープにusingディレクティブを記述するのは推奨できない。特に、ヘッダーファイルのグローバルスコープにusingディレクティブを記述すると、非常に問題が多い。名前空間の本来の目的は、名前の衝突を防ぐためである。usingディレクティブは、名前空間という仕組みに穴を開けるような機能だからだ。



しかし、usingディレクティブは必要である。たとえば、非常に長い名前空間名や、深くネストした名前空間内の多数のメンバーを使う場合、いちいち::演算子で明示的にスコープを指定したり、using宣言でひとつひとつ宣言していくのは、非常に面倒である。あるブロックスコープで、名前が衝突しないということが保証できるならば、usingディレクティブを使っても構わない。



.. code-block:: c++
  
  namespace really_long_name { namespace yet_another_long_name
  {
      int a ; int b ; int c ; int d ;  
  } }
  
  void f()
  {
      // このスコープでは、a, b, c, dという名前は衝突しないと保証できる
      using namespace really_long_name::yet_another_long_name ;
      a = 0 ; b = 0 ; c = 0 ; d = 0 ;
  }


usingディレクティブは、宣言ではない。usingディレクティブは、非修飾名前探索に、名前を探すべき名前空間を、特別に追加するという機能を持っている。したがって、usingディレクティブは、名前を隠さない。以下の例はエラーである。<a href="#namespace.udecl">using宣言</a>と比較すると、違いがある。



.. code-block:: c++
  
  int name  ; // グローバルスコープのname
  namespace NS { int name ; } // NS名前空間のname
  
  int main()
  {
      // ここではまだ、名前が隠されてはいない
      name = 0 ; // ::nameを意味する
  
      using namespace NS ; // 名前探索にNS名前空間内のメンバーを追加
      name = 0 ; // エラー、::nameとNS::nameとで、どちらを使うべきか曖昧
  }


usingディレクティブは、非修飾名前探索にしか影響を与えない。ADLには影響を与えない。



<p class="editorial-note">
TODO: range-based forで使われているトリックも記述。



.. code-block:: c++
  
  namespace NS
  {
      struct S { } ;
      namespace inner
      { 
          void f(S) { }
          void g(S) { }
      }
  
      using inner::f ; // inner::fをNS名前空間に導入する
      using namespace inner ; // 非修飾名前探索に影響をおぼよす
  } ;
  
  int main()
  {
      NS::S s ;
      f(s) ; // OK
      g(s) ; // エラー、usingディレクティブはADLには影響しない
  }


usingディレクティブで探索できるようになった名前は、オーバーロード関数の候補にもなる。



.. code-block:: c++
  
  void f( int ) { } 
  namespace NS { void f( double ) { } }
  
  int main()
  {
      // この時点では、NS::fは名前探索で発見されない
      f( 1.23 ) ; // ::f(int)
  
      using namespace NS ; // NS名前空間のメンバーがunqualified名前探索で発見されるようになる
      f( 1.23 ) ; // オーバーロード解決により、NS::f( double )
  }


usingディレクティブは、unqualified名前探索のルールを変更するという、非常に特殊な機能である。usingディレクティブは、確実に名前が衝突しないブロックスコープ内で使うか、あるいは、オーバーロード解決をさせるので、同じ関数名を複数、意図的に名前探索で発見させる場合にのみ、使うべきである。




リンケージ指定（Linkage specifications）
--------------------------------------------------------------------------------



関数型、外部リンケージを持つ関数名、外部リンケージを持つ変数名には、言語リンケージ（language linkage）という概念がある。リンケージ指定（Linkage specification）は、言語リンケージを指定するための文法である。リンケージ指定と、<a href="#dcl.stc">ストレージクラス指定子</a>のextern指定子とは、別物である。



注意、実装依存の話：言語リンケージは、C++と他のプログラミング言語との間での、関数名や変数名の相互利用のための機能である。異なる言語間で名前を相互利用するには、共通の仕組みが必要である。これには、たとえば名前マングリングを始めとして、レジスターの使い方、引数のスタックへの積み方などの様々な要素がある。しかし、これらはいずれも本書の範疇を超えるので解説しない。



.. code-block:: c++
  
  extern 文字列リテラル { 宣言リスト }
  extern 文字列リテラル 宣言


標準では、C++言語リンケージと、C言語リンケージを定めている。C++の場合、文字列リテラルは"C++"となり、C言語の場合、文字列リテラルは"C"となる。何も指定しない場合、デフォルトでC++言語リンケージとなる。異なるリンケージ指定がされた名前は、たとえその他のシグネチャーがすべて同じであったとしても、別の型として認識される。その他の文字列がどのような扱いを受けるかは、実装依存である。



.. code-block:: c++
  
  // 関数型へのC言語リンケージの指定
  extern "C" typedef void function_type() ;
  // 関数名へのC言語リンケージの指定
  extern "C" int f() ;
  // 変数名へのC言語リンケージの指定
  extern "C" int value ;


{ }を使う方のリンケージ指定子は、複数の宣言に対して、一括して言語リンケージを指定するための文法である。




.. code-block:: c++
  
  // 関数名f, g, hは、すべてC言語リンケージを持つ
  extern "C"
  {
      void f() ;
      void g() ;
      void h() ;
  }
  
  // C_functions.hというヘッダーファイルで宣言されているすべての関数型、関数名、変数名は、C言語リンケージを持つ
  extern "C"
  {
      #include "C_functions.h"
  }


リンケージ指定をしない場合、デフォルトでC++言語リンケージだとみなされる。通常、C++言語リンケージを指定する必要はない。



.. code-block:: c++
  
  // デフォルトのC++言語リンケージ
  void g() ;
  // 明示的な指定
  extern "C++" void g() ;


リンケージ指定はネストすることができる。その場合、一番内側のリンケージ指定が使われる。言語リンケージは、スコープをつくらない。



.. code-block:: c++
  
  extern "C"
  {
      void f() ; // C言語リンケージ
      extern "C++"
      {
          void g() ; // C++言語リンケージ
      }
  }


リンケージ指定は、名前空間スコープの中でのみ、使うことができる。ブロックスコープ内などでは使えない



C言語リンケージは、クラスのメンバーに適用しても無視される。



.. code-block:: c++
  
  extern "C"
  {
      class C
      {
          void f() ; // C++言語リンケージ
      } ;
  }


C言語リンケージを持つ同名の関数が、複数あってはならない。これにより、C言語リンケージを持つ関数は、オーバーロードできない。



.. code-block:: c++
  
  extern "C"
  {
  // エラー、C言語リンケージを持つ同名の関数が複数ある
      void f(int) ;
      void f(double) ;
  }
  
  // OK、互いに異なる言語リンケージを持つ
  void g() ;
  extern "C" void g() ;


このルールは、たとえ関数が名前付きの名前空間の中で宣言されていても、同様である。



.. code-block:: c++
  
  namespace A
  {
      extern "C" void f() ;
  }
  
  namespace B
  {
      extern "C" void f() ; // エラー、A::fとB::fは同じ関数を参照する
      void f() ; // OK、C++言語リンケージを持つ
  }


このように、たとえ名前空間が違ったとしても、C言語リンケージを持つ関数は、名前が衝突してはならない。これは、名前空間という仕組みが存在しないC言語からでも使えるようにするための仕様である。ただし、C言語リンケージを持つ関数を、C++側から、名前空間の中で宣言して、通常通り使うことはできる。



.. code-block:: c++
  
  namespace NS
  {
      extern "C" void f() { }
  }
  
  int main()
  {
  
      NS::f() ; // OK
  }


これにより、C言語で書かれた関数を、何らかの名前空間の中にいれて、C++側から使うこともできる。



.. code-block:: c++
  
  // ヘッダーファイル、C_functions.hは、C言語で書かれているものとする
  namespace obsolete_C_lib
  {
      extern "C"
      {
          #include "C_functions.h"
      }
  }


アトリビュート（Attributes）
--------------------------------------------------------------------------------



<p class="editorial-note">
TODO:attributeは変更される動きが見られるので保留。


