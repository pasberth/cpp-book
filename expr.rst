式（Expressions）
================================================================================

優先順位と評価順序
--------------------------------------------------------------------------------



TODO: 式の優先順位の評価順序の表は必要か。詳しく分かったところで何か実用上の意味はあるのか。



式には、優先順位と評価順序がある。



優先順位とは、ある式の中で、異なる式が複数使われた場合、どちらが先に評価されるのかという順位である。この優先順位は、人間にとって自然になるように設計されているので、通常、式の優先順位を気にする必要はない。



.. code-block:: c++
  
  // 1 + (2 * 3)
  // operator *が優先される
  1 + 2 * 3 ;
  
  int x ;
  // operator +が優先される
  x = 1 + 1 ;


評価順序とは、ある式の中で、優先順位の同じ式が複数使われた場合、どちらを先に評価するかという順序である。これは、式ごとに、「左から右（Left-To-Right）」、あるいは「右から左（Right-To-Left）」のどちらかになる。



たとえば、operator +は、「左から右」である。



.. code-block:: c++
  
  // (1 + 1) + 1 と同じ
  1 + 1 + 1 ;


一方、operator = は、「右から左」である。



.. code-block:: c++
  
  int x ; int y ;
  // x = (y = 0) と同じ
  x = y = 0 ;


これも、人間にとって自然になるように設計されている。通常、気にする必要はない。


未評価オペランド（unevaluated_operand）
--------------------------------------------------------------------------------



<a href="#expr.typeid">typeid演算子</a>、<a href="#expr.sizeof">sizeof演算子</a>、<a href="#expr.unary.noexcept">noexcept演算子</a>、<a href="#dcl.type.simple">decltype型指定子</a>では、あるいは未評価オペランド（unevaluated_operand）というものが使われる。このオペランドは文字通り、評価されない式である。



オペランドの式は評価されないが、式を評価した結果の型は、通常の評価される式と何ら変わりない。



.. code-block:: c++
  
  int f()
  {
      std::cout << "hello" << std::endl ;
      return 0 ;
  }
  
  int main()
  {
      // int x ; と同等
      // 関数fは呼ばれない
      decltype( f() ) x ;
  }


この例では、オペランドの式の結果の型を、変数xとして宣言、定義している。関数呼び出しの結果の型は、関数の戻り値の型になるので、型はintである。ただし、式自体は評価されないので、実行時に関数が呼ばれることはない。つまり、標準出力にhelloと出力されることはない。



この未評価式は、評価されないということを除けば、通常の式と全く同じように扱われる。例えば、オーバーロード解決やテンプレートのインスタンス化なども、通常の式と同じように働く。



.. code-block:: c++
  
  // 関数の宣言だけでいい。定義は必要ない
  double f(int) ;
  int f(double) ;
  
  int main()
  {
      // double x ; と同等
      decltype( f(0) ) x ;
      // int y ; と同等
      decltype( f(0.0) ) y ;
  }


この例では、関数fは、宣言だけされていて、定義がない。しかし、これは全く問題がない。なぜならば、未評価式は評価されないので、関数fが呼ばれることはない。呼ばれることがなければ、定義も必要はない。


一次式（Primary expressions）
--------------------------------------------------------------------------------



一次式には、多くの細かな種類がある。例えば、リテラルや名前も一次式である。ここでは、一次式の中でも、特に重要なものを説明する。



:: 演算子
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



:: 演算子は、ある名前のスコープを指定する演算子である。このため、非公式に「スコープ解決演算子」とも呼ばれている。しかし、公式の名前は、:: 演算子(operator ::)である。::に続く名前のスコープは、::の前に指定されたスコープになる。



.. code-block:: c++
  
  // スコープはグローバル
  int x = 0;
  
  // スコープはNS名前空間
  namespace NS { int x = 0; }
  
  // スコープはCクラス
  struct C { static int x ; } ;
  int C::x = 0 ;
  
  
  int main()
  {// スコープはmain()関数のブロック
      int x = 0 ;
  
      x ; // ブロック
  
      ::x ; // グローバル
      NS::x ; // NS名前空間
      C::x ; // クラス
  }


このように、::に続く名前のスコープを指定することができる。スコープが省略された場合は、グローバルスコープになる。



式の結果は、::に続く名前が、関数か変数の場合はlvalueに、それ以外はprvalueになる。




括弧式（parenthesized expression）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



括弧式とは、括弧である。これは、式を囲むことができる。括弧式の結果は、括弧の中の式とまったく同じになる。これは主に、ひとつの式の中で、評価する順序を指定するような場合に用いられる。あるいは、単にコードを分かりやすく、強調するために使っても構わない。



.. code-block:: c++
  
  (0) ; // 括弧式
  
  // 1 + (2 * 3) = 1 + 6 = 7
  1 + 2 * 3 ;
  // 3 * 3 = 9
  (1 + 2 ) * 3


ほとんどの場合、括弧式の有無は、括弧の中の式の結果に影響を与えない。ただし、括弧式の有無によって意味が変わる場合もある。例えば、decltype指定子だ。




ラムダ式（Lambda expressions）
--------------------------------------------------------------------------------



ラムダ式（lambda expression）は、関数オブジェクトを簡単に記述するための式である。以下のような文法になる



.. code-block:: c++
  
  [ ラムダキャプチ

ラムダ式の基本的な使い方
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



ラムダ式を、通常の関数のように使う方法を説明する。まず、ラムダ式の構造は、以下のようになっている。



.. code-block:: c++
  
  [/*ラムダキャプチャー*/] // ラムダ導入子
  (/*仮引数リスト*/) // 省略可能
  -> void // 戻り値の型、省略可能
  {} // 複合文


これを、通常の関数定義と比較してみる。



.. code-block:: c++
  
  auto // 関数宣言
  func // 関数名
  () // 引数リスト
  -> void // 戻り値の型
  {} // 関数の定義


ラムダ式は、関数オブジェクトである。通常の関数のように、引数もあれば、戻り値もある。もちろん、通常の関数のように、何も引数に取らないこともできるし、戻り値を返さないこともできる。



.. code-block:: c++
  
  // 通常の関数
  auto f() -> void {}
  // ラムダ式
  []() -> void {} ;


ラムダ式を評価した結果は、prvalueの一時オブジェクトになる。この一時オブジェクトを、クロージャーオブジェクト（closure object）と呼ぶ。クロージャーオブジェクトの型は、クロージャー型（closure type）である。クロージャー型はユニークで、名前がない。これは実装依存の型であり、ユーザーは具体的な型を知ることができない。このクロージャーオブジェクトは、関数オブジェクトと同じように振舞う。



.. code-block:: c++
  
  auto f = []() ->void {} ;


ラムダ式は関数オブジェクトなので、通常の関数と同じように、operator ()を適用することで呼び出すことができる。



.. code-block:: c++
  
  // 通常の関数
  auto f() -> void {}
  
  int main()
  {
      f() ; // 関数の呼び出し
  
      // ラムダ式
      auto g = []() -> void {} ;
      g() ; // ラムダ式の呼び出し
  
      // ラムダ式を直接呼び出す
      []() -> void {}() ;
  }


仮引数リストと、戻り値の型は、省略できる。従って、最小のラムダ式は、以下の通りになる。



.. code-block:: c++
  
  []{}


仮引数リストを省略した場合は、引数を取らないということを意味する。戻り値の型を省略した場合は、ラムダ式の複合文の内容によって、戻り値の型が推測される。複合文が以下の形になっている場合、



.. code-block:: c++
  
  { return 式 ; }


戻り値の型は、式に lvalueからrvalueへの型変換、 配列からポインターへの型変換、関数からポインターへの型変換を適用した結果の型になる。



それ以外の場合は、void型になる。



注意しなければならないことは、戻り値の型を推測させるためには、複合文は必ず、{ return 式 ; }の形でなければならない。つまり、return文ひとつでなければならないということだ。return文以外に、複数の文がある場合、戻り値の型はvoidである。



.. code-block:: c++
  
  // エラー、戻り値の型はvoidだが、値を返している
  []
  {
      int x = 0 ;
      return x ;
  }() ;
  
  
  // OK、戻り値の型を、明示的に指定している。
  [] -> int
  {
      int x = 0 ;
      return x ;
  }() ;


いくつか例を挙げる。



.. code-block:: c++
  
  // 戻り値の型はint
  auto type1 = []{ return 0 ; }() ;
  
  // 戻り値の型はdouble
  auto type2 = []{ return 0.0 ; }() ;
  
  // 戻り値の型はvoid
  []{ }() ;
  []
  {
      int x = 0 ;
      x = 1 ;
  }() ;


ラムダ式の引数は、通常の関数と同じように記述できる。



.. code-block:: c++
  
  int main()
  {
      auto f = []( int a, float b ) { return a ; }
      f( 123, 3.14f ) ;
  }


複合文は、通常の関数の本体と同じように扱われる。



.. code-block:: c++
  
  int main()
  {
      // 通常の関数と同じように文を書ける
      auto f =
          [] { 
              int x = 0 ;
              ++x ;
          }
      f() ;
  
      auto g = []
      {// もちろん、複数の文を書ける
          int x = 0 ;
          ++x ; ++x ; ++x ;
      } ;
  
      g() ;
  }


クロージャーオブジェクトは、変数として保持できる。



.. code-block:: c++
  
  #include <functional>
  
  int main()
  {
      // auto指定子を使う方法 
      auto f = []{} ;
      f() ;
  
      // std::functionを使う方法
      std::function< void (void) > g = []{} ;
      g() ;
  }


ラムダ式は、テンプレート引数にも渡せる。



.. code-block:: c++
  
  template < typename Func >
  void f( Func func )
  {
      func() ;// 関数オブジェクトを呼び出す
  }
  
  int main()
  {
      f( []{ std::cout << "hello" << std::endl ; } ) ;
  }


ラムダ式の使い方の例を示す。例えば、std::vectorの全要素を、標準出力に出力したいとする。



.. code-block:: c++
  
  #include <iostream>
  #include <vector>
  
  struct Print
  {
      void operator () ( int value ) const
      { std::cout << value << std::endl ; }
  } ;
  
  int main()
  {
      std::vector<int> v = { 1, 2, 3, 4, 5 } ;
      std::for_each( v.begin(), v.end(), Print() ) ;  
  }


この例では、本質的にはたった一行のコードを書くのに、わざわざ関数オブジェクトを、どこか別の場所に定義しなければならない。ラムダ式を使えば、その場に書くことができる。



.. code-block:: c++
  
  #include <vector>
  #include <algorithm>
  
  int main()
  {
      std::vector<int> v = { 1, 2, 3, 4, 5 } ;
      std::for_each( v.begin(), v.end(),
          [](int value){ std::cout << value << std::endl ; } ) ;  
  }


変数のキャプチャー
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



関数内に関数を書くことができるのは、確かに手軽で便利だ。しかし、ラムダ式は、単にその場に関数を書くだけでは終わらない。ラムダ式は、関数のローカル変数をキャプチャーできる。



.. code-block:: c++
  
  #include <iostream>
  
  template < typename Func >
  void call ( Func func )
  {
      func() ;// helloと表示する
  }
  
  int main()
  {
      std::string str = "hello" ;
      // main関数のローカル変数strを、ラムダ式の中で使う
      auto f = [=]{ std::cout << str << std::endl ; } ;
      f() ;
      // もちろん、他の関数に渡せる。
      call( f ) ;
  }


このように、ラムダ式が定義されている関数のブロックスコープの中のローカル変数を、使うことができる。この機能を、変数のキャプチャーという。



この、ラムダ式で、定義されている場所のローカル変数を使えるというのは、一見、奇妙に思えるかもしれない。しかし実のところ、これは単なるシンタックスシュガーにすぎない。同じことは、従来の関数オブジェクトでも行える。詳しくは後述する。



もちろん、クロージャーオブジェクトがどのように実装されるかは、実装により異なる。しかし基本的に、ラムダ式は、このような関数オブジェクトへの、シンタックスシュガーに過ぎない。



[]の中身を、ラムダキャプチャーという。ラムダキャプチャーの中には、キャプチャーリストを記述できる。変数のキャプチャーをするには、キャプチャーリストに、どのようにキャプチャーをするかを指定しなければならない。変数のキャプチャーには、二種類ある。コピーでキャプチャーするか、リファレンスでキャプチャーするかの違いである。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      // コピーキャプチャー
      [=] { x ; }
      // リファレンスキャプチャー
      [&] { x ; }
  }


キャプチャーリストに=を記述すると、コピーキャプチャーになる。&amp;を記述すると、リファレンスキャプチャーになる。



コピーキャプチャーの場合、変数はクロージャーオブジェクトのデータメンバーとして、コピーされる。リファレンスキャプチャーの場合は、クロージャーオブジェクトに、変数への参照が保持される。



コピーキャプチャーの場合は、ラムダ式から、その変数を書き換えることができない。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      [=]
      {// コピーキャプチャー
          int y = x ; // OK、読むことはできる
          x = 0 ; // エラー、書き換えることはできない
      } ;
  
      [&]
      {// リファレンスキャプチャー
          int y = x ; // OK
          x = 0 ; // OK
      } ;
  }


これは、クロージャーオブジェクトのoperator()が、const指定されているためである。ラムダ式にmutableが指定されていた場合、operator()は、const指定されないので、書き換えることができる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      [=]() mutable
      {
          int y = x ; // OK
          x = 0 ; // OK
      } ;
  }


リファレンスキャプチャーの場合は、変数の寿命に気をつけなければならない。



.. code-block:: c++
  
  #include <functional>
  
  int main()
  {
      std::function< void ( void ) > f ;
      std::function< void ( void ) > g ;
  
  
      {
          int x = 0 ;
          f = [&]{ x ; } ; // リファレンスキャプチャー
          g = [=]{ x ; } ; // コピーキャプチャー
      }
  
      f() ;// エラー、xの寿命は、すでに尽きている。
  
      g() ; // OK
  }


ローカル変数の寿命は、そのブロックスコープ内である。この例で、fを呼び出すときには、すでに、xの寿命は尽きているので、エラーになる。



ラムダ式がキャプチャーできるのは、ラムダ式が記述されている関数の、最も外側のブロックスコープ内である。



.. code-block:: c++
  
  int main()
  {// 関数の最も外側のブロックスコープ
      int x ;
      {
          int y ;
  
          // xもyもキャプチャーできる。
          [=]{ x ; y ; } ;
      }
  }


関数の最も外側のブロックスコープ以外のスコープ、例えばグローバル変数などは、キャプチャーせずにアクセス出来る。



.. code-block:: c++
  
  // グローバルスコープの変数
  int x = 0 ;
  
  int main()
  {
      // キャプチャーする必要はない
      []{ x ; } ;
  }


変数ごとに、キャプチャー方法を指定できる。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ;
      int b = 0 ;
  
      [ a, &b ]{} ;
  }


変数のキャプチャー方法を、それぞれ指定する場合、キャプチャーリストの中に、変数名を記述する。その時、単に変数名だけを記述した場合、コピーキャプチャーになり、変数名の前に&amp;をつけた場合、リファレンスキャプチャーになる。



キャプチャーしたい変数がたくさんある場合、いちいち名前をすべて記述するのは面倒であるので、デフォルトのキャプチャー方法を指定できる。これをデフォルトキャプチャー（default capture）という。この時、デフォルトキャプチャーに続けて、個々の変数名のキャプチャー方法を指定できる。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ; int b = 0 ; int c = 0 ; int d = 0 ; 
  
      // デフォルトはコピーキャプチャー
      [=]{ a ; b ; c ; d ; } ;
      // デフォルトはリファレンスキャプチャー
      [&]{ a ; b ; c ; d ; } ;
  
      // aのみリファレンスキャプチャー
      [=, &a]{} ;
  
      // aのみコピーキャプチャー
      [&, a]{} ;
  
      // a, bのみリファレンスキャプチャー
      [=, &a, &b]{} ;
  
      // デフォルトキャプチャーを使わない
      [a]{} ;
  }


このとき、デフォルトキャプチャーと同じキャプチャー方法を、個々のキャプチャーで指定することはできない。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ; int b = 0 ;
  
      // エラー、デフォルトキャプチャーと同じ
      [=, a]{} ;
      // OK
      [=, &a]{} ;
  
      // エラー、デフォルトキャプチャーと同じ
      [&, &a]{} ;
      // OK
      [&, a]{} ;
  }


キャプチャーリスト内で、同じ名前を複数書くことはできない。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      // エラー
      [x, x]{} ;
  }


たとえ、キャプチャー方法が同じであったとしても、エラーになる。



デフォルトキャプチャーが指定されているラムダ式の関数の本体で、キャプチャーできる変数を使った場合、その変数は、暗黙的にキャプチャーされる。



変数のキャプチャーの具体的な使用例を示す。今、vectorの各要素の合計を求めるプログラムを書くとする。関数オブジェクトで実装をすると、以下のようになる。



.. code-block:: c++
  
  struct Sum
  {
      int sum ;
      Sum() : sum(0) { }
      void operator ()( int value )
      { sum += value ; std::cout << sum << std::endl ; }
  } ;
  
  int main()
  {
      std::vector<int> v = {1,2,3,4,5} ;
      Sum sum = std::for_each( v.begin(), v.end(), Sum() ) ;
  
      std::cout << sum.sum << std::endl ;
  }


これは、明らかに分かりにくい。sum += valueという短いコードのために、関数オブジェクトを定義しなければならないし、その取扱も面倒である。このため、多くのプログラマは、STLのアルゴリズムを使うより、自前のループを書きたがる。



.. code-block:: c++
  
  int main()
  {
      std::vector<int> v = {1,2,3,4,5} ;
      int sum = 0 ;
      for ( auto iter = v.begin() ; iter != v.end() ; ++iter )
      {
          sum += *iter ;
      }
  
      std::cout << sum << std::endl ;
  }


しかし、ループを手書きするのは分かりにくいし、間違いの元である。ラムダ式のキャプチャーは、この問題を解決してくれる。



.. code-block:: c++
  
  int main()
  {
      std::vector<int> v = {1,2,3,4,5} ;
      int sum = 0 ;
      std::for_each( v.begin(), v.end(),
          [&]( int value ){ sum += value ; }
      ) ;
  
      std::cout << sum << std::endl ;
  }


これで、コードは分かりやすくなる。また、ループを手書きしないので、間違いも減る。






ラムダ式の詳細
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



クロージャーオブジェクト（closure object）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ラムダ式が評価された結果は、クロージャーオブジェクト（closure object）になる。これは、一種の関数オブジェクトで、その型は、ユニークで無名な実装依存のクラスであるとされている。この型は、非常に限定的にしか使えない。例えば、ラムダ式は、未評価式の中で使うことが出来ない。これは、decltypeやsizeofの中で使うことが出来ないということを意味する。



.. code-block:: c++
  
  using type = decltype([]{}) ; // エラー
  sizeof([]{}) ; // エラー
  
  // OK
  auto f = []{} ;


クロージャーオブジェクトがどのように実装されるかは、実装依存である。しかし、今、説明のために、実装の一例を示す。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ; int b = 0 ;
      auto f = [a, &b](){ a ; b ; } ;
      f() ;
  }


例えば、このようなコードがあったとすると、例えば、以下のように実装できる。



.. code-block:: c++
  
  class Closure // 本来、ユーザー側から使える名前は存在しない
  {
  private :
      // aはコピーキャプチャー、bはリファレンスキャプチャー
      int a ; int & b ;
  public :    
      Closure(int & a, int & b )
          : a(a), b(b) { }
  
      // コピーコンストラクターが暗黙的に定義される
      Closure( Closure const & ) = default ;
      // ムーブコンストラクターが暗黙的に定義される可能性がある
      Closure( Closure && ) = default ;
  
      // デフォルトコンストラクターはdelete定義される
      Closure() = delete ;
      // コピー代入演算子はdelete定義される
      Closure & operator = ( Closure const & ) = delete ;
      
      
  
      inline void operator () ( void ) const
      { a ; b ; }
  } ;
  
  int main()
  {
      int a = 0 ; int b = 0 ;
      auto f = Closure(a, b) ;
      f() ;
  }


クロージャーオブジェクトは、メンバー関数として、operator ()を持つ。これにより、関数呼び出しの演算子で、関数のように呼び出すことができる。キャプチャーした変数は、データメンバーとして持つ。このoperator ()は、inlineである。また、mutable指定されていない場合、const指定されている。これにより、コピーキャプチャーした変数は、書き換えることができない。mutableが指定されている場合、constではなくなるので、書き換えることができる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      // エラー
      [x]() { x = 0 ; } ;
      // OK
      [x]() mutable { x = 0 ;} ;
  }




ラムダ式の仮引数リストには、デフォルト引数を指定できない。



.. code-block:: c++
  
  // エラー
  [](int x = 0){} ;


ラムダ式は、例外指定できる。



.. code-block:: c++
  
  []() noexcept {} ;


ラムダ式に例外指定をすると、クロージャーオブジェクトのoperator ()に、同じ例外指定がなされたものと解釈される。



クロージャーオブジェクトには、コピーコンストラクターが暗黙的に定義される。ムーブコンストラクターは、可能な場合、暗黙的に定義される。デフォルトコンストラクターと、コピー代入演算子は、delete定義される。これはつまり、初期化はできるが、コピー代入はできないということを意味する。



.. code-block:: c++
  
  // 初期化はできる。
  auto f = []{} ;
  
  // OK fはラムダ式ではないので可能
  using closure_type decltype(f) ;
  // OK 初期化はできる
  closure_type g = f ;
  
  // エラー、デフォルトコンストラクターは存在しない
  closure_type h ;
  // エラー、コピー代入演算子は存在しない。
  h = f ;


関数ポインターへの変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

ラムダキャプチャーを使わないラムダ式のクロージャーオブジェクトは、同一の引数と戻り値の関数ポインターへの変換関数を持つ。



.. code-block:: c++
  
  void (*ptr1)(void) = []{} ;
  auto (*ptr2)(int, int, int) -> int = [](int a, int b, int c) -> int { return a + b + c ; }
  
  // 呼び出す。
  ptr1() ; ptr2() ;


ラムダキャプチャーを使っているクロージャーオブジェクトは、関数ポインターに変換できない。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ; 
      // エラー、変換できない
      auto (*ptr1)(void) -> int = [=] -> int{ return x ; } ;
      auto (*ptr2)(void) -> int = [&] -> int{ return x ; } ;
  }


変数をキャプチャーしないラムダ式というのは、関数オブジェクトではなく、単なる関数に置き換えることができるので、このような機能が提供されている。この機能は、まだテンプレートを使っていない既存のコードやライブラリとの相互利用のために用意されている。



ラムダ式のネスト
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

ラムダ式はネストできる。



.. code-block:: c++
  
  []{// 外側のラムダ式
      []{} ;// 内側のラムダ式
  } ;


この時、問題になるのは、変数のキャプチャーだ。内側のラムダ式は、外側のラムダ式のブロックスコープから見える変数しか、キャプチャーすることはできない。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ; int b = 0 ;
      [b]{// 外側のラムダ式
          int c = 0 ;
          [=]{// 内側のラムダ式
              a ; // エラー、aはキャプチャーできない。
              b ; // OK
              c ; // OK
          } ;
      } ;
  }


外側のラムダ式が、デフォルトキャプチャーによって、暗黙的に変数をキャプチャーしている場合は、内側のラムダも、その変数をキャプチャーできる。



.. code-block:: c++
  
  int main()
  {
      int a = 0 ;
      [=]{// 外側のラムダ式
          [=]{// 内側のラムダ式
              a ; // OK
          } ;
      } ;
  }




thisのキャプチャー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



基本的にラムダ式は、そのラムダ式が使われているブロックスコープのローカル変数しかキャプチャーできない。しかし、実は、データメンバーを使うことができる。



.. code-block:: c++
  
  struct C
  {
      int x ;
      void f()
      {
          [=]{ x ; } ;// OK、ただし、これはキャプチャーではないことに注意
      }
  } ;


このように、非staticなメンバー関数のラムダ式では、データメンバーを使うことができる。しかし、これは、データメンバーをキャプチャーしているわけではない。その証拠に、データメンバーを直接キャプチャーしようとすると、エラーになる。



.. code-block:: c++
  
  struct C
  {
      int x ;
      void f()
      {
          [x]{} ; // エラー、データメンバーはキャプチャーできない
      }
  } ;


では、どうしてデータメンバーが使えるのか。一体何をキャプチャーしているのか。実は、これはthisをキャプチャーしているのである。ラムダ式は、thisをキャプチャーできる。



.. code-block:: c++
  
  struct C
  {
      int x ;
      void f()
      {
          [this]{ this->x ; } ;
      }
  } ;


ラムダ式の関数の本体では、thisは、クロージャーオブジェクトへのポインターではなく、ラムダ式が使われている非staticなメンバー関数のthisをキャプチャーしたものと解釈される。thisは、必ずコピーキャプチャーされる。というのも、そもそもthisはポインターなので、リファレンスキャプチャーしても、あまり意味はない。



.. code-block:: c++
  
  struct C
  {
      int x ;
      void f()
      {
          [this]{} ; // OK
          [&this]{} ; // エラー、thisはリファレンスキャプチャーできない
      }
  } ;


ラムダ式にデフォルトキャプチャーが指定されていて、データメンバーが使われている場合、thisは暗黙的にキャプチャーされる。デフォルトキャプチャーがコピーでもリファレンスでも、thisは必ずコピーキャプチャーされる。



.. code-block:: c++
  
  struct C
  {
      int x ;
      void f()
      {
          [=]{ x ; } ; // thisをコピーキャプチャーする
          [&]{ x ; } ; // thisをコピーキャプチャーする
      }
  } ;


thisのキャプチャーは、注意を要する。すでに述べたように、データメンバーは、キャプチャーできない。ラムダ式でデータメンバーを使うということは、thisをキャプチャーするということである。データメンバーは、thisを通して使われる。これは、データメンバーは参照で使われるということを意味する。ということは、もし、クロージャーオブジェクトのoperator ()が呼ばれた際に、thisを指し示すオブジェクトが無効になっていた場合、エラーとなってしまう。



.. code-block:: c++
  
  struct C
  {
      int x ;
      std::function< int (void) > f()
      {
          return [this]{ return x ; } ;
      }
  } ;
  
  int main()
  {
      std::function< int (void) > f ;
      {
          C c ;
          f = c.f() ;
      }// cの寿命はすでに終わっている
  
      f() ;// エラー
  }


データメンバーをコピーキャプチャーする方法はない。そもそも、何度も述べているように、データメンバーはキャプチャーできない。では、上の例で、どうしてもデータメンバーの値を使いたい場合はどうすればいいのか。この場合、一度ローカル変数にコピーするという方法がある。



.. code-block:: c++
  
  struct C
  {
      int x ;
      std::function< int (void) > f()
      {
          int x = this->x ;
          return [x]{ return x ; } ;// xはローカル変数のコピー
      }
  } ;


もちろん、同じ名前にするのが紛らわしければ、名前を変えてもいい。



ラムダ式でデータメンバーを使う際には、キャプチャーしているのは、実はthisなのだということに注意しなければならない。




パラメーターパックのキャプチャー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



可変引数テンプレートの関数パラメーターパックも、キャプチャーリストに書くことができる。その場合、通常と同じように、パック展開になる。



.. code-block:: c++
  
  template < typename ... Types > void g( Types ... args ) ;
  
  template < typename ... Types >
  void f( Types ... args )
  {
      // 明示的なキャプチャー
      [args...]{ g( args... ) ; } ;
      [&args...]{ g( args... ) ; } ;
  
      // 暗黙的なキャプチャー
      [=]{ g( args... ) ; } ;
      [&]{ g( args... ) ; } ;   
  }




後置式（Postfix expressions）
--------------------------------------------------------------------------------



後置式は、主にオペランドの後ろに演算子を書くことから、そう呼ばれている。後置式の評価順序はすべて、「左から右」である。



添字（Subscripting）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  式 [ 式 ]
  式 [ 初期化リスト ]


operator []は、添字と呼ばれる式である。これは、配列の要素にアクセスするために用いられる。どちらか片方の式は、Tへのポインター型でなければならず、もう片方は、unscoped enumか、整数型でなければならない。式の結果は、lvalueのTとなる。式、E1[E2] は、*((E1)+(E2)) と書くのに等しい



.. code-block:: c++
  
  int x[3] ;
  // *(x + 1)と同じ
  x[1] ;


この場合、xには、<a href="#conv.array">配列からポインターへの型変換</a>が適用されている。



「どちらか片方の式」というのは、文字通り、どちらか片方である。たとえば、x[1]とすべきところを、1[x]としても、同じ意味になる。



.. code-block:: c++
  
  int x[3] ;
  // どちらも同じ意味。
  x[1] ;
  1[x] ;


もっとも、通常は、一つめの式をポインター型にして、二つ目の式を整数型にする。ユーザー定義のoperator []では、このようなことはできない。



ユーザー定義のoperator []の場合、[]の中の式に、初期化リストを渡すことができる。これは、どのように使ってもいいいが、例えば以下のように使える。



.. code-block:: c++
  
  struct C
  {
      int data[10][10][10] ;
      int & operator []( std::initializer_list<std::size_t> list )
      {
          if ( list.size() != 3 ){/* エラー処理 */}
  
          auto iter = list.begin() ;
          std::size_t const i = *iter ; ++iter ;
          std::size_t const j = *iter ; ++iter ;
          std::size_t const k = *iter ;
          
          return data[i][j][k] ;
      }
  } ;
  
  int main()
  {
      C c ;
      c[{1, 2, 3}] = 0 ;
  }


初期化リストを使えば、オーバーロードされたoperator []に、複数の引数を渡すことができる。




関数呼び出し（Function call）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数呼び出し（function call）の文法は、以下の通り。



.. code-block:: c++
  
  式 ( 引数のリスト )


関数呼び出しには、通常の関数呼び出しと、メンバー関数呼び出しがある。



通常の関数を呼び出す場合、式には、関数へのlvalueか、関数へのポインターが使える。



.. code-block:: c++
  
  void f( void ) { } 
  void g( int ) { } 
  void h( int, int, int ) { } 
  
  int main()
  {
      // 「関数へのlvalue」への関数呼び出し
      f( ) ;
      g( 0 ) ;
      h( 0, 0, 0 ) ;
  
      // 関数への参照
      void (&ref)(void) = f ;
  
      // 「関数へのlvalue」への関数呼び出し
      ref() ;
  
      // 関数ポインター
      void (*ptr)(void) = &f ;
  
      // 関数ポインターへの関数呼び出し
      ptr() ;
  }


staticなメンバー関数は、通常の関数呼び出しになる。



.. code-block:: c++
  
  struct C { static void f(void) {} } ;
  
  int main()
  {
      void (*ptr)(void) = &C::f ;
      ptr() ; // 通常の関数呼び出し
  }


メンバー関数を呼び出す場合、式には、関数のメンバーの名前か、メンバー関数へのポインター式が使える。



.. code-block:: c++
  
  struct C
  {
      void f(void) {}
  
      void g(void)
      {
          // メンバー関数の呼び出し
          f() ;
          this->f() ; 
          (*this).f() ;
  
          // メンバー関数へのポインター
          void (C::* ptr)(void) = &C::f ;
          // 関数呼び出し
          (this->*ptr)() ;
      }
  } ;


関数呼び出し式の結果の型は、式で呼び出した関数の戻り値の型になる。



.. code-block:: c++
  
  void f() ;
  int g() ;
  
  // 式の結果の型はvoid
  f() ;
  // 式の結果の型はint
  g() ;


関数呼び出しの結果の型は、戻り値の型になる。これはtypeidやsizeofやdecltypeのオペランドの中でも、同様である。



.. code-block:: c++
  
  // 関数fの戻り値の型はint
  // すなわち、fを関数呼び出しした結果の型はint
  int f() { return 0 ; }
  
  int main()
  {
      // sizeof(int)と同じ
      sizeof( f() ) ;
      // typeid(int)と同じ
      typeid( f() ) ;
      // int型の変数xの宣言と定義。
      decltype( f() ) x ;
  }


関数が呼ばれた際、仮引数は対応する実引数で初期化される。非staticメンバー関数の場合、this仮引数もメンバー関数を呼び出した際のオブジェクトへのポインターで初期化される。



仮引数に対して、具体的な一時オブジェクトが生成されるかどうかは、実装依存である。たとえば、実装は最適化のために、一時オブジェクトの生成を省略するかもしれない。



仮引数が参照の場合をのぞいて、呼ばれた関数の中で仮引数を変更しても、実引数は変更されない。ただし、型がポインターの場合、参照を通して参照先のオブジェクトが変更される可能性がある。



.. code-block:: c++
  
  void f( int x, int & ref, int * ptr )
  {
      x = 1 ; // 実引数は変更されない
      ref = 1 ; // 実引数が変更される
      *ptr = 1 ; // 実引数は、ポインターの参照を通して変更される
      ptr = nullptr ; // 実引数のポインターは変更されない
  }
  
  int main()
  {
      int x = 0 ;// 実引数
      int * ptr = &x ;
      f( x, x, ptr ) ;
  }


実引数の式が、どのような順番で評価されるかは決められていない。ただし、呼び出された関数の本体に入る際には、式はすべて評価されている。



.. code-block:: c++
  
  #include <iostream>
   
  int f1(){ std::cout << "f1" << std::endl ; return 0 ; }
  int f2(){ std::cout << "f2" << std::endl ; return 0 ; }
  int f3(){ std::cout << "f3" << std::endl ; return 0 ; }
  
  void g( int, int, int ){ }
  
  int main( )
  {
      g( f1(), f2(), f3() ) ;// f1, f2, f3関数呼び出しの順番は分からない
  }


この例では、関数f1, f2, f3がどの順番で呼ばれるのかが分からない。したがって、標準出力にどのような順番で文字列が出力されるかも分からない。ただし、関数gの本体に入る際には、f1, f2, f3は、すべて呼び出されている。



関数は、自分自身を呼び出すことができる。これを再帰呼び出しという。



.. code-block:: c++
  
  void f()
  {
      f() ; // 自分自身を呼び出す、無限ループ
  }


ただし、main関数だけは特別で、再帰呼び出しをすることができない。



.. code-block:: c++
  
  int main()
  {
      main() ; // エラー
  }




関数形式の明示的型変換（Explicit type conversion (functional notation)）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  型名 ( 式リスト )
  型名 初期化リスト


関数形式の明示的型変換（Explicit type conversion (functional notation)）とは、関数呼び出しのような文法による、一種のキャストである。



.. code-block:: c++
  
  struct S
  {
      S( int ) { }
      S( int, int ) { }
  } ;
  
  int main()
  {
      int() ;
      int{} ;
  
      S( 0 ) ;
      S( 1, 2 ) ;
  }


型名として使えるのは、<a href="#dcl.type.simple">単純型指定子</a>か、typename指定子である。単純型指定子でなければならないということには、注意しなければならない。たとえば、ポインターやリファレンス、配列などを直接書くことはできない。ただし、typedef名は使える。



.. code-block:: c++
  
  int x = 0 ;
  // これらはエラー
  int *(&x) ;
  int &(x) ;
  
  // typedef名は使える
  using type = int * ;
  type(&x) ;


単純型指定子の中でも、autoとdecltypeは、注意が必要である。まず、autoは使えない。



.. code-block:: c++
  
  auto(0) ; // エラー


decltypeは使える。ただし、非常に使いづらいので、使うべきではない。



.. code-block:: c++
  
  // int型をint型にキャスト
  // int(0) と同じ
  decltype(0)(0) ;


たとえば、以下のコードはエラーである。



.. code-block:: c++
  
  int x ;
  decltype(x)(x) ;// エラー


これは、文法が曖昧だからだ。詳しくは、<a href="#stmt.ambig">曖昧解決</a>を参照。何が起こっているかというと、decltype(x)(x)は、キャストではなく、変数の宣言だとみなされている。decltype(x)は、intという型である。



.. code-block:: c++
  
  // decltype(x)(x) と同じ
  // decltype(x)(x) → int (x) → int x
  int x ;


このため、decltypeを関数形式のキャストで使うのは、問題が多い。使うならば、typedef名をつけてから使うか、static_castを使うべきである。



.. code-block:: c++
  
  int x ;
  using type = decltype(x) ;
  type(x) ;
  
  static_cast< decltype(x) >(x) ;


typename指定子も使うことができる。



.. code-block:: c++
  
  template < typename T >
  void f()
  {
      typename T::type() ; // OK
  }


式リストが、たったひとつの式である場合、<a href="#expr.cast">キャスト</a>と同じ意味になる。



.. code-block:: c++
  
  // int型からshort型へのキャスト
  short(0) ;
  // int型からdouble型へのキャスト
  double(0) ;
  
  struct C { C(int) {} } ;
  // 変換関数による、int型からC型へのキャスト
  C(0) ; 


型名がクラス名である場合、T(x1, x2, x3)という形の式は、T t(x1, x2, x3)という形と同じ意味を持つ一時オブジェクトを生成し、その一時オブジェクトを、prvalueの結果として返す。型名がクラス名でも、式リストがひとつしかない場合は、キャストである。もっとも、その場合も、ユーザー定義のコンストラクターが、変換関数として呼び出されることになるので、意味はあまり変わらない。



.. code-block:: c++
  
  struct C
  {
      C(int) {}
      C(int, int) {}
      C(int, int, int) {}
  } ;
  
  int main()
  {
      C(0) ; // これはキャスト、意味としては、あまり違いはない
      C(1, 2) ; 
      C(1, 2, 3) ;
  }


式リストが空の場合、つまり、T()という形の式の場合。まず、Tは配列型であってはならない。Tは完全な型か、voidでなければならない。式の結果は、値初期化された型のprvalueの値になる。値初期化については、<a href="#dcl.init">初期化子</a>を参照。



.. code-block:: c++
  
  int() ; // int型の0で初期化された値
  double() : // double型の0で初期化された値
  
  struct C {} ;
  C() ;// デフォルトコンストラクターが呼ばれたCの値


void型の場合、値初期化はされない。式の結果の型はvoidである。



.. code-block:: c++
  
  void() ; // 結果はvoid


括弧で囲まれた式リストではなく、初期化リストの場合、式の結果は、指定された型の、初期化リストによって直接リスト初期化されたprvalueの一時オブジェクトになる。



.. code-block:: c++
  
  #include <initializer_list>
  
  struct C
  {
      C( std::initializer_list<int> ) { }
  } ;
  
  int main()
  {
      C{1,2,3} ;
  }




疑似デストラクター呼び出し（Pseudo destructor call）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



疑似デストラクター呼び出しとは、デストラクターを明示的に呼び出すことができる一連の式である。使い方は、operator .、operator -&gt;に続けて、疑似デストラクター名を書き、さらに関数呼び出しのoperator ()を書く。この一連の式を、疑似ですトラクター呼び出しという。このような疑似デストラクター名に続けては、関数呼び出し式しか適用することができない。式の結果はvoidになる。



.. code-block:: c++
  
  // このコードは、疑似デストラクター呼び出しの文法を示すためだけの例である
  struct C {} ;
  
  int main()
  {
      C c ;
      c.~C() ; // 疑似デストラクター呼び出し
      C * ptr = &c
      ptr->~C() ;// 疑似デストラクター呼び出し
  }


注意すべきことは、デストラクターを明示的に呼び出したとしても、暗黙的に呼び出されるデストラクターは、依然として呼び出されるということである。



.. code-block:: c++
  
  #include <iostream>
  
  struct C
  {
      ~C() { std::cout << "destructed." << std::endl ; }
  } ;
  
  int main()
  {
      {
          C c ;
          c.~C() ;// デストラクターを呼び出す
      }// ブロックスコープの終りでも、デストラクターは暗黙的に呼ばれる
  
      C * ptr = new C ;
      ptr->~C() ;// デストラクターを呼び出す
  
      delete ptr ;// デストラクターが暗黙的に呼ばれる。
  }


このように、通常は、デストラクターの呼び出しが重複してしまう。二重にデストラクターを呼び出すのは、大抵の場合、プログラム上のエラーである。では、疑似デストラクター呼び出しは何のためにあるのか。具体的な用途としては、placement newと組み合わせて使うということがある。



.. code-block:: c++
  
  struct C { } ;
  
  int main()
  {
      // placement new用のストレージを確保
      void * storage = operator new( sizeof(C) ) ;
      // placement new
      C * ptr =  new(storage) C ;
      // デストラクターを呼び出す
      ptr->~C() ;
      // placement new用のストレージを解放
      operator delete( storage ) ;
  }


この疑似デストラクターには、decltypeを使うことができる。



.. code-block:: c++
  
  struct C {} ;
  
  int main()
  {
      C c ;
      c.~decltype(c) ; 
      C * ptr = &c
      ptr->~decltype(c) ;
  }


テンプレート引数の場合、型がスカラー型であっても、疑似デストラクター呼び出しができる



.. code-block:: c++
  
  template < typename T >
  void f()
  {
      T t ;
      t.~T() ;
  }
  
  int main()
  {
      f<int>() ;
  }


これにより、ジェネリックなテンプレートコードが書きやすくなる。




クラスメンバーアクセス（Class member access）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



TODO: 詳細なvalue categoryを説明するかどうか。



.. code-block:: c++
  
  クラスのオブジェクト . メンバー名
  クラスのポインター -> メンバー名


クラスメンバーアクセスは、名前の通り、クラスのオブジェクトか、クラスのオブジェクトへのポインターのメンバーにアクセスするための演算子である。



. 演算子の左側の式は、クラスのオブジェクトでなければならない。-&gt; 演算子の左側の式は、クラスのオブジェクトへのポインターでなければならない。演算子の右側は、そのクラスか、基本クラスのメンバー名でなければならない。-&gt; 演算子を使った式、E1-&gt;E2は、(*(E1)).E2という式とおなじになる。



.. code-block:: c++
  
  struct Object
  {
      int x ;
      static int y ;
      void f() {}
  } ;
  
  int Object::y ;
  
  int main()
  {
      Object obj ;
      // . 演算子
      obj.x = 0 ;
      obj.y = 0 ;
      obj.f() ;
  
      Object * ptr = &obj ;
      // -> 演算子
      ptr->x = 0 ;
      ptr->y = 0 ;
      ptr->f() ;
  }


もし、クラスのオブジェクト、クラスのオブジェクトへのポインターを表す式が依存式であり、メンバー名がメンバーテンプレートであり、テンプレート引数を明示的に指定したい場合、メンバー名の前に、templateキーワードを使わなければならない。



.. code-block:: c++
  
  struct Object
  {
      template < typename T >
      void f() {}
  } ;
  
  template < typename T >
  void f()
  {
      T obj ;
      obj.f<int>() ; // エラー
      obj.template f<int>() ; // OK
  }
  
  int main()
  {
      f<Object>() ;
  }


これは、&lt;演算子や、&gt;演算子と、文法が曖昧になるためである。この問題については、<a href="#temp.names">テンプレート特殊化の名前</a>でも、解説している。



派生によって、クラスのメンバー名が曖昧な場合、エラーになる。



.. code-block:: c++
  
  struct Base1 { int x ; } ;
  struct Base2 { int x ; } ;
  
  struct Derived : Base1, Base2
  { } ;
  
  int main()
  {
      Derived d ;
  
      d.x ; // エラー    
      d.Base1::x ;// OK
      d.Base2::x ;// OK
  }


TODO: value categoryについて。むしろlvalue and rvalueのところで説明すべきか




インクリメントとデクリメント（Increment and decrement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



ここでは、後置式のインクリメントとデクリメントについて解説する。前置式のインクリメントとデクリメントについては、<a href="#expr.pre.incr">単項式のインクリメントとデクリメント</a>を参照。



.. code-block:: c++
  
  式 ++
  式 --


後置式の++演算子の式の結果は、オペランドの式の値になる。オペランドは、変更可能なlvalueでなければならない。オペランドの型は、数値型か、ポインター型でなければならない。式が評価されると、オペランドに1を加算する。ただし、式の結果は、オペランドに1を加算する前の値である。



.. code-block:: c++
  
  int x = 0 ;
  int result = x++ ;
  
  // ここで、result == 0, x == 1


式の結果の値は、オペランドの値と変わりがないが、オペランドには、1を加算されるということに注意しなければならない。



後置式の--演算子は、オペランドから1を減算する。それ以外は、++演算子と全く同じように動く。



.. code-block:: c++
  
  int x = 0 ;
  int result = x-- ;
  
  // ここで、result == 0, x == -1




Dynamic cast（Dynamic cast）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  dynamic_cast < 型名 > ( 式 )


dynamic_cast&lt;T&gt;(v)という式は、vという式をTという型に変換する。便宜上、vをdynamic_castのオペランド、Tをdynamic_castの変換先の型とする。変換先の型はクラスへのポインターかリファレンス、あるいは、voidへのポインター型でなければならない。オペランドは、変換先の型が、ポインターの場合はポインター、リファレンスの場合はリファレンスでなければならない。



.. code-block:: c++
  
  struct C {} ;
  
  int main()
  {
      C c ;
  
      // 変換先の型がポインターの場合は、オペランドもポインター
      // 変換先の型がリファレンスの場合は、オペランドもリファレンスでなければならない
      dynamic_cast<C &>(c) ; // OK
      dynamic_cast<C *>(&c) ; // OK
  
      // ポインターかリファレンスかが、一致していない
      dynamic_cast<C *>(c) ; // エラー
      dynamic_cast<C &>(&c) ; // エラー 
  }


dynamic_castの機能
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



今、Derivedクラスが、Baseクラスから派生されていたとする。



.. code-block:: c++
  
  struct Base {} ;
  struct Derived : Base {} ;


この時、static_castを使えば、Baseへのポインターやリファレンスから、Derivedへのポインターやリファレンスに変換することができる。



.. code-block:: c++
  
  int main()
  {
      Derived d ;
  
      Base & base_ref = d ;
      Derived & derived_ref = static_cast<Derived &>(base_ref) ;
  
      Base * base_ptr = &d ;
      Derived * derived_ptr = static_cast<Derived *>(base_ptr) ;
  }


この例では、ポインターやリファレンスが指す、本当のオブジェクトは、Derivedクラスのオブジェクトだということが分かりきっているので安全である。しかし、ポインターやリファレンスを使う場合、常にオブジェクトの本当のクラス型が分かるわけではない。



.. code-block:: c++
  
  void f( Base & base )
  {
      // baseがDerivedを参照しているかどうかは、分からない。
      Derived & d = static_cast<Derived &>(base) ;
  }
  
  int main()
  {
      Derived derived ;
      f(derived) ; // ok
  
      Base base ;
      f(base) ; // エラー
  }


このように、ポインターやリファレンスの指し示すオブジェクトの本当のクラス型は、実行時にしか分からない。しかし、オブジェクトの型によって、特別な処理をしたいことも、よくある。



.. code-block:: c++
  
  void f( Base & base )
  {
      if ( /* baseの指すオブジェクトがDerivedクラスの場合*/ )
      {
          // 特別な処理
      }
  
      // 共通の処理
  }


本来、このような処理は、virtual関数で行うべきである。しかし、現実には、どうしても、このような泥臭くて汚いコードを書かなければならない場合もある。そのようなどうしようもない場合のために、C++には、基本クラスへのポインターやリファレンスが、実は派生クラスをオブジェクトを参照している場合に限り、キャストできるという機能が提供されている。それが、dynamic_castである。




動的な型チェックを使うためには、dynamic_castのオペランドのクラスは、ポリモーフィック型でなければならない。つまり、すくなくともひとつのvirtual関数を持っていなければならない。ポリモーフィック型の詳しい定義については、<a href="#class.virtual">virtual関数</a>を参照。



もし、オペランドの参照するオブジェクトが、変換先の型として指定されている派生クラスのオブジェクトであった場合、変換することができる。



.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base {} ;
  
  void f(Base & base)
  {// baseはDerivedを指しているとする
      Derived & ref = dynamic_cast<Derived &>(base) ;
      Derived * ptr = dynamic_cast<Derived *>(&base) ;
  }


実引数に、変換先の型ではないオブジェクトを渡した場合、dynamic_castの変換は失敗する。変換が失敗した場合、変換先の型がリファレンスの場合、std::bad_castがthrowされる。変換先の型がポインターの場合、nullポインターが返される。



.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base {} ;
  
  int main()
  {
      Base base ;
  
      // リファレンスの場合
      try {
          Derived & ref = dynamic_cast<Derived &>(base) ;
      } catch ( std::bad_cast )
      {
          // 変換失敗
          // リファレンスの場合、std::bad_castがthrowされる
      }
  
      // ポインターの場合
      Derived * ptr = dynamic_cast<Derived *>(&base) ;
  
      if ( ptr == nullptr )
      {
          // 変換失敗
          // ポインターの場合、nullポインターが返される
      }
  }


基本クラスのポインターやリファレンスが、実際は何を指しているかは、実行時にしか分からない。そのため、常に変換に失敗する可能性がある。そのため、dynamic_castを使う場合は、常に変換が失敗するかもしれないという前提のもとに、コードを書かなければならない。



失敗せずに変換できる場合というのは、オペランドの指すオブジェクトの本当の型が、変換先の型のオブジェクトである場合で、しかもアクセスできる場合である。オブジェクトである（is a）場合というのは、例えば、



.. code-block:: c++
  
  struct A { virtual void f(){} } ;
  struct B : A {} ;
  struct C : B {} ;
  struct D : C {} ;


このようなクラスがあった場合、Dは、Cであり、Bであり、Aである。従って、Dのオブジェクトを、Aへのリファレンスで保持していた場合、D、C、Bのいずれにも変換できる。



.. code-block:: c++
  
  int main()
  {
      D d ;
      A & ref = d ;
  
      // OK
      // refの指しているオブジェクトは、Dなので、変換できる。
      dynamic_cast<D &>(ref) ;
      dynamic_cast<C &>(ref) ;
      dynamic_cast<B &>(ref) ;    
  }


アクセスできる場合というのは、変換先の型から、publicで派生している場合である。



.. code-block:: c++
  
  struct Base1 { virtual void f(){} } ;
  struct Base2 { virtual void g(){} } ;
  struct Base3 { virtual void h(){} } ;
  
  struct Derived
      : public Base1,
        public Base2,
        private Base3
  { } ;
  
  int main()
  {
      Derived d ;
      Base1 & ref = d ;
  
      // OK、Base2はpublicなので、アクセス出来る
      dynamic_cast<Base2 &>(ref) ;
      // 実行時エラー、Base3はprivateなので、アクセス出来ない
      // std::bad_castがthrowされる。
      dynamic_cast<Base3 &>(ref) ;
  }


この例の場合、refが参照するオブジェクトは、Derived型であるので、Base3型のサブオブジェクトも持っているが、Base3からは、privateで派生されているために、アクセスすることはできない。そのため、変換することが出来ず、std::bad_castがthrowされる。



変換先の型は、void型へのポインターとすることもできる。その場合、オペランドの指す本当のオブジェクトの、もっとも派生されたクラスを指すポインターが、voidへのポインター型として、返される。



.. code-block:: c++
  
  struct Base { virtual void f(){} } ;
  struct Derived1 : Base {} ;
  struct Derived2 : Derived1 {} ;
  
  int main()
  {
      Derived1 d1 ;
      Base * d1_ptr = &d1 ;
  
      // Derived1を指すポインターの値が、void *として返される
      void * void_ptr1 = dynamic_cast<void *>(d1_ptr) ;
  
      Derived1 d2 ;
      Base * d2_ptr = &d2;
  
      // Derived2を指すポインターの値が、void *として返される
      void * void_ptr2 = dynamic_cast<void *>(d2_ptr) ;
  }


一般に、この機能はあまり使われることがないだろう。



dynamic_castのその他の機能
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



dynamic_castは、その主目的の機能の他にも、クラスへのポインターやリファレンスに限って、キャストを行うことができる。この機能は、<a href="#conv.ptr">標準型変換のポインターの型変換</a>に、ほぼ似ている。このキャストは、static_castでも行える。以下の機能に関しては、実行時のコストは発生しない。



オペランドの型が、変換先の型と同じ場合、式の結果の型は、変換先の型になる。この時、constとvolatileを付け加えることはできるが、消し去ることは出来ない。



.. code-block:: c++
  
  // 型と式が同じ場合の例
  struct C { } ;
  
  int main()
  {
      C v ;
  
      dynamic_cast<C &>(v) ;
      dynamic_cast<C const &>(v) ; // constを付け加える
  
      C const cv ;
      dynamic_cast<C &>(cv) ;// エラー、constを消し去ることは出来ない
  
      // ポインターの場合 
      C * ptr = &v ;
      dynamic_cast<C *>(ptr) ;   
      dynamic_cast<C const *>(ptr) ;
  }


変換先の型が基本クラスへのリファレンスで、オペランドの型が、派生クラスへのリファレンスの場合、dynamic_castの結果は、派生クラスのうちの基本クラスを指すリファレンスになる。ポインターの場合も、同様である。



.. code-block:: c++
  
  struct Base {} ; // 基本クラス
  struct Derived : Base {} ; // 派生クラス
  
  int main()
  {
      Derived d ;
  
      Base & base_ref = dynamic_cast<Base &>(d) ;
      Base * base_ptr = dynamic_cast<Base *>(&d) ;
  }






型識別（Type identification）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  typeid ( 式 )
  typeid ( 型名 )


typeidとは、式や型名の、型情報を得るための式である。型情報は、const std::type_infoのリファレンスという形で返される。std::type_infoについての詳細は、<a href="#support.rtti">RTTI（Run Time Type Information）</a>を参照。typeidを使うには、必ず、&lt;typeinfo&gt;ヘッダーを#includeしなければならない。ただし、本書のサンプルコードは、紙面の都合上、必要なヘッダーのincludeを省略していることがある。



typeidのオペランドは、sizeofに似ていて、式と型名の両方を取ることができる。



.. code-block:: c++
  
  #include <typeinfo>
  
  int main()
  {
      // 型名の例
      typeid(int) ;
      typeid( int * ) ;
  
      // 式の例
      int x = 0 ;
      typeid(x) ; 
      typeid(&x) ;
      typeid( x + x ) ;
  
  }


typeidのオペランドの式が、ポリモーフィッククラス型のglvalueであった場合、実行時チェックが働き、結果のstd::type_infoが表す型情報は、実行時に決定される。型情報は、オブジェクトの最も派生したクラスの型となる。



.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base {} ;
  
  int main()
  {
      Derived d ;
      Base & ref = d ;
  
      // オブジェクトの、実行時の本当の型を表すtype_infoが返される
      std::type_info const & ti = typeid(d) ;
  
      // true
      ti == typeid(Derived) ;
  
      // Derivedを表す、人間の読める実装依存の文字列
      std::cout << ti.name() << std::endl ;
  }


オペランドの式の型がポリモーフィッククラス型のglvalueの場合で、nullポインターを参照した場合は、std::bad_typeidが投げられる。



.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base {} ;
  
  int main()
  {
      // ptrの値はnullポインター
      Base * ptr = nullptr ;
  
      try {
          typeid( *ptr ) ;// 実行時エラー
      } catch( std::bad_typeid )
      {
          // 例外が投げられて、ここに処理が移る
      }
  }


オペランドの式の型が、ポリモーフィッククラス型でない場合は、std::type_infoが表す型情報は、コンパイル時に決定される。



.. code-block:: c++
  
  // int型を表すtype_info
  typeid(0) ;
  // double型を表すtype_info
  typeid(0.0) ;
  
  int f() {}
  // int型を表すtype_info
  typeid( f() ) ;


この際、<a href="#conv.lval">lvalueからrvalueへの型変換</a>、<a href="#conv.array">配列からポインターへの型変換</a>、<a href="#conv.func">関数からポインターへの型変換</a>は行われない。



.. code-block:: c++
  
  // 配列からポインターへの型変換は行われない
  int a[10] ;
  
  // 型情報は、int [10]
  // int *ではない
  typeid(a) ;
  
  // 関数からポインターへの型変換は行われない
  void f() {}
  
  // 型情報は、void (void)
  // void (*)(void)ではない。
  typeid(f) ;


これらの標準型変換は、C++では、非常に多くの場所で、暗黙のうちに行われているので、あまり意識しない。たとえば、テンプレートの実引数を推定する上では、これらの変換が行われる。



.. code-block:: c++
  
  // 実引数の型を、表示してくれるはずの便利な関数
  template < typename T >
  void print_type_info(T)
  {
      std::cout << typeid(T).name() << std::endl ;
  }
  
  void f() { }
  
  int main()
  {
      int a[10] ;
      // int [10]
      std::cout << typeid(a).name() << std::endl ;
      // int *
      print_type_info(a) ;
  
      // void (void)
      std::cout << typeid(f).name() << std::endl ;
      // void (*)(void)
      print_type_info(f) ;
  }


std::type_info::name()の返す文字列は実装依存だが、今、C++の文法と同じように型を表示すると仮定すると、このような出力になる。C++では、多くの場面で、暗黙のうちに、これら三つの型変換が行われるので、このような差異が生じる。



オペランドが、型名の場合は、std::type_infoは、その型を表す。ほんの一例をあげると。



.. code-block:: c++
  
  int main()
  {
      typeid( int ) ;             // int型
      typeid( int * ) ;           // intへのポインター型
      typeid( int & ) ;           // intへのlvalueリファレンス型
      typeid( int [2] ) ;         // 配列型
      typeid( int (*)[2] ) ;      // 配列へのポインター型
      typeid( int (int) ) ;       // 関数型
      typeid( int (*)(int) );     // 関数へのポインター型
  }


オペランドの式や型名の、トップレベル（top-level）のCV修飾子は、無視される。



.. code-block:: c++
  
  int main()
  {
      // トップレベルのCV修飾子は無視される
      typeid(const int) ; // int
      // 当然、型情報は等しい
      typeid(const int) == typeid(int) ; // true
  
      // 型名も式も同じ
      int i = 0 ; const int ci = 0;
      typeid(ci) ; // int
      typeid(ci) == typeid(i) ; // true
  
      // これはトップレベルのCV修飾子
      typeid(int * const) ; // int *
  
      // 以下はトップレベルのCV修飾子ではない
      typeid(const int *) ; // int const *
      typeid(int const *) ; // int const *
  }




Static cast（Static cast）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  static_cast< 型名 >( 式 )


static_castは、実に多くの静的な変換ができる。その概要は、標準型変換とその逆変換、ユーザー定義の変換、リファレンスやポインターにおける変換など、比較的安全なキャストである。以下にstatic_castの行える変換を列挙するが、これらを丸暗記しておく必要はない。もし、どのキャストを使うか迷った場合は、static_castを使っておけば、まず間違いはない。static_castがコンパイルエラーとなるキャストは、大抵、実装依存で危険なキャストである。



static_castによるキャストがどのように行われるかは、おおむね、以下のような順序で判定される。条件に合う変換方法が見つかった時点で、それより先に行くことはない。これは、完全なstatic_castの定義ではない。分かりやすさのため省いた挙動もある。



static_cast&lt;T&gt;(v)の結果は、オペランドvを変換先の型Tに変換したものとなる。変換先の型がlvalueリファレンスならば結果はlvalue、rvalueリファレンスならば結果はxvalue、それ以外の結果はprvalueとなる。static_castは、constとvolatileを消し去ることはできない。





オペランドの型が基本クラスで、変換先の型が派生クラスへのリファレンスの場合。もし、標準型変換で、派生クラスのポインターから、基本クラスのポインターへと変換できる場合、キャストできる。



.. code-block:: c++
  
  struct Base {} ;
  struct Derived : Base {} ;
  
  void f(Base & base)
  {
      // Derived *からBase *に標準型変換で変換できるので、キャストできる
      Derived & derived = static_cast<Derived &>(base) ;
  }


ただし、これには実行時チェックがないので、baseが本当にDerivedのオブジェクトを参照していなかった場合、動作は未定義である。



glvalueのオペランドは、rvalueリファレンスに型変換できる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      static_cast<int &&>(x) ;
  }


もし、static_cast&lt;T&gt;(e) という式で、T t(e); という宣言ができる場合、オペランドの式eは、変換先の型Tに変換できる。その場合、一時オブジェクトを宣言して、それをそのまま使うのと、同じ意味になる。



.. code-block:: c++
  
  // short t(0) は可能なので変換できる
  static_cast<short>(0) ;
  
  // float t(0) は可能なので変換できる
  static_cast<float>(0) ;


<a href="#conv">標準型変換</a>の逆変換を行うことができる。ただし、いくつかの変換は、逆変換を行えない。これには、<a href="#conv.lval">lvalueからrvalueへの型変換</a>、<a href="#conv.array">配列からポインターへの型変換</a>、<a href="#conv.func">関数からポインターへの型変換（Function-to-pointer conversion）</a>、ポインターや関数ポインターからnullポインターへの変換、がある。



変換先の型に、voidを指定することができる。その場合、static_castの結果はvoidである。オペランドの式は評価される。



.. code-block:: c++
  
  int main()
  {
      static_cast<void>( 0 ) ;
      static_cast<void>( 1 + 1 ) ;    
  } 


整数型とscoped enum型は、static_castを使うことで、明示的に変換することができる。その場合、変換先の型で、オペランドの値を表現できる場合は、値が保持される。値を表現できない場合の挙動は、規定されていない。



.. code-block:: c++
  
  int main()
  {
      enum struct A { value = 1 } ;
      enum struct B { value = 1 } ;
  
      int x = static_cast<int>( A::value ) ;
      A a = static_cast<A>(1) ;
      B b = static_cast<B>( A::value ) ;
  } 


派生クラスへのポインターから、基本クラスへのポインターにキャストできる。



.. code-block:: c++
  
  struct Base {} ;
  struct Derived : Base {} ;
  
  Derived d ;
  Base * ptr = static_cast<Base *>(&d) ;


voidへのポインターは、他の型へのポインターに変換できる。ある型へのポインターから、voidへのポインターにキャストされ、そのまま、ある型へのポインターにキャストされなおされた場合、その値は保持される。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      int * ptr = &x ;
  
      // void *への変換は、標準型変換で行えるので、キャストはなくてもよい。
      void * void_ptr = static_cast<void *>(ptr) ;
  
      // キャストが必要
      ptr = static_cast<int *>(void_ptr) ;
  
      *ptr ; // ポインターの値は保持されるので、xを正しく参照する
  } 




Reinterpret cast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  reinterpret_cast < 型名 > ( 式 )


reinterpret_castは、式の値をそのまま、他の型に変換するキャストである。ポインターと整数の間の変換や、ある型へのポインターを全く別の型へのポインターに変換するといったことができる。reinterpret_castを使えば、値をそのままにして、型を変換することができる。変換した結果、その値が、変換先の型としてそのまま使えるかどうかなどといったことは、ほとんど規定されていない。元の値をそのまま保持できるかどうかも分からない。それ故、reinterpret_castは、危険なキャストである。



多くの実装では、reinterpret_castには、何らかの具体的で実用的な意味がある。現実のC++が必要とされる環境では、reinterpret_castを使わなければならないことも、多くある。しかし、reinterpret_castを使った時点で、そのコードは実装依存であり、具体的に意味が定義されたその環境でしか動かないということを、常に意識するべきである。



reinterpret_castでは、constやvolatileを消し去ることはできない。



reinterpret_castでできる変換を、以下に列挙する。



ポインター型と整数型の間の型変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ある型へのポインター型から整数型へのキャスト、あるいはその逆に、整数型やenum型からポインター型へのキャストを行える。整数型は、ポインターの値をそのまま保持できるほど大きくなければならない。どの整数型ならば十分に大きいのか。もし整数型が十分に大きくなければどうなるのかなどということは、定義されていない。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      int * ptr = &x ;
  
      // ポインターから整数へのキャスト
      int value = reinterpret_cast<int>(ptr) ;
  
      // 整数からポインターへのキャスト
      ptr = reinterpret_cast<int *>(value) ;
  } 


これらのキャストについての挙動は、ほとんどが実装依存であり、あまり説明できることはない。



もし、変換先の整数型が、ポインターの値をすべて表現できるとするならば、再びポインター型にキャストし直した時、ポインターは同じ値を保持すると規定されている。しかし、int型がポインターの値をすべて表現できるという保証はない。unsigned intであろうと、long intであろうとlong long intであろうと、そのような保証はない。従って、上記のコードで、ptrが同じ値を保つかどうかは、実装依存である。




異なるポインター型の間の型変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ある型へのポインターは、まったく別の型へのポインターに変換できる。たとえば、int *からshort *などといった変換ができる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
      int * int_ptr = &x ;
  
      // int * からshort *へのキャスト
      short * short_ptr = reinterpret_cast<short *>(int_ptr) ;
  } 


これについても、挙動は実装依存であり、特に説明できることはない。たとえば、上記のコードで、short_ptrを参照した場合どうなるのかということも、全く規定されていない。ある実装では、問題なく、int型のストレージを、あたかもshort型のストレージとして使うことができるかもしれない。ある実装では、参照した瞬間にプログラムがクラッシュするかもしれない。




異なるリファレンス型の間の型変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



異なるポインター型の間の型変換に似ているが、異なるリファレンス型の変換をすることができる。例えば、int &amp;からshort &amp;などといった変換ができる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      // int & からshort &へのキャスト
      short & short_ref = reinterpret_cast<short &>(x) ;
  } 


異なるポインター型の間の型変換と同じで、これについても、具体的な意味は実装依存である。




異なるメンバーポインターの間の型変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



異なるメンバーポインターへ変換することができる。



.. code-block:: c++
  
  struct A { int value ; } ;
  struct B { int value ; } ;
  
  int main()
  {
      int B::* ptr = reinterpret_cast<int B::*>(&A::value) ;
  } 


意味は、実装依存である。




異なる関数ポインター型の間の型変換
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



ある関数ポインターは、別の型の関数ポインターにキャストできるかもしれない。意味は実装依存である。「かもしれない」というのは実に曖昧な表現だが、たとえ完全に規格準拠な実装であっても、この機能をサポートする義務がないという意味である。



.. code-block:: c++
  
  void f(int) {}
  
  int main()
  {
      // void (short)な関数へのポインター型
      using type = void (*)(short) ;
  
      // 関数ポインターの型変換
      type ptr = reinterpret_cast<type>(&f) ;
  } 


この変換がどういう意味を持つのか。例えば、変換した結果の関数ポインターは、関数呼び出しできるのか。できるとして、一体どういう意味になるのか、などということは一切規定されていない。




reinterpret_castには、できないこと
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



reinterpret_castが行えるキャストは、上記にすべて列挙した。それ以外の変換は、reinterpret_castでは行うことができない。これは、そもそもreinterpret_castの目的が、危険で実装依存なキャストのみを分離するという目的にあるので、それ以外の変換は、あえて行えないようになっている。



.. code-block:: c++
  
  int main()
  {
      short value = 0 ;
  
      // OK、標準型変換による暗黙の型変換
      int a = value ;
      // OK、static_castによる明示的な型変換
      int b = static_cast<int>(value) ;
  
      // エラー
      // reinterpret_castでは、この型変換をサポートしていない
      int c = reinterpret_cast<int>(value) ;
  } 






Const cast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  const_cast < 型名 > ( 式 )


const_castは、constとvolatileが異なる型の間の型変換を行う。constやvolatileを取り除くことや、付け加えることができる。



.. code-block:: c++
  
  int main()
  {
      int const x = 0 ;
  
      // エラー、constを取り除くことはできない。
      int * error1 = &x ; 
      int * error2 = static_cast<int *>(&x) ;
  
      // OK、ポインターの例
      int * ptr = const_cast<int *>(&x) ;
      // OK、リファレンスの例
      int & ref = const_cast<int &>(x) ;
  
      // constを付け加えることもできる。
      int y = 0 ;
      int const * cptr = const_cast<int const *>(&y) ;
  } 


ポインターへのポインターであっても、それぞれのconstを取り除くことができる。



.. code-block:: c++
  
  int main()
  {
      int const * const * const * const c = nullptr ;
      int *** ptr = const_cast<int ***>(c) ;
  } 


const_castは、constやvolatileのみを取り除く、または付け加えるキャストのみを行える。それ以外の型変換を行うことはできない。



.. code-block:: c++
  
  int main()
  {
      int const x = 0 ;
      // エラー、const以外の型変換を行っている。
      short * ptr = const_cast<short *>(&x) ;
  } 


では、constを取り除くと同時に、他の型変換も行ないたい場合はどうするかというと、static_castや、reinterpret_castを併用する。



.. code-block:: c++
  
  int main()
  {
      int const x = 0 ;
  
      short * ptr1 =
          static_cast<short *>(
              static_cast<void *>(
                  const_cast<int *>(&x)
              )
          ) ;
    
      short * ptr2 = reinterpret_cast<short *>(const_cast<int *>(&x)) ;
  } 


const_castは、基本的に、ほとんどのconstをキャストすることができるが、キャストできないconstも存在する。たとえば、関数ポインターやメンバー関数ポインターに関するconstを取り除くことはできない。関数へのリファレンスも同様である。



.. code-block:: c++
  
  void f( int ) {}
  
  int main()
  {
      using type = void (*)(int) ;
      type const ptr = nullptr ;
  
      // エラー、関数ポインターはキャストできない
      type p = const_cast<type>(ptr) ;
  } 


もちろん、関数の仮引数に対するconstをキャストすることや、constなメンバー関数を非constなメンバー関数にキャストすることなどもできない。




単項式（Unary expressions）
--------------------------------------------------------------------------------



単項式は、オペランドをひとつしか取らないことより、そう呼ばれている。単項式の評価順序はすべて、「右から左」である。



単項演算子（Unary operators）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



単項演算子というカテゴリーには、五つの異なる演算子がまとめられている。*、&amp;、+、-、!、~である。



* 演算子と& 演算子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



* 単項演算子は、参照（indirection）である。オペランドは、オブジェクトへのポインターでなければならない。オペランドの型が、「Tへのポインター」であるとすると、式の結果は、lvalueのTである。



&amp; 演算子は、オペランドのポインターを得る。オペランドの型がTであるとすると、結果は、prvalueのTへのポインターである。&amp; 演算子は、オブジェクトだけではなく、関数にも適用できる。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      // & 演算子
      // 変数xのオブジェクトへのポインターを得る。
      int * ptr = &x ;
  
      // * 演算子
      // ポインターを参照する
      *ptr ;
  }




単項演算子の+と-
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



単項演算子の+と-は、オペランドの符号を指定する演算子である。



+ 単項演算子は、オペランドの値を、そのまま返す。オペランドの型には、数値型、非scoped enum型、ポインター型が使える。結果はprvalueである。



.. code-block:: c++
  
  int main()
  {
      int x = +0 ; // xは0
      +x ; // 結果は0
  
      int * ptr = nullptr ;
      +ptr ; // 結果はptrの値
  } 


ただし、オペランドには、整数のプロモーションが適用されるので、オペランドの型がcharやshort等の場合、int型になる。



.. code-block:: c++
  
  short x = 0 ;
  +x ; // int型の0


- 単項演算子は、オペランドの値を、負数にして返す。オペランドの型には、数値型と非scoped enum型が使える。+ 単項演算子と同じく、オペランドには整数のプロモーションが適用される。



.. code-block:: c++
  
  -0 ; // 0
  -1 ; // -1
  - -1 ; // +1


- 単項演算子が、unsignedな整数型に使われた場合の挙動は、明確に定義されている。オペランドのunsignedな整数型のビット数をnとする。式の結果は、2<sup>n</sup>から、オペランドの値を引いた結果の値になる。



具体的な例を挙げるために、今、unsigned int型を16ビットだと仮定する。



.. code-block:: c++
  
  // unsigned int型は16bitであるとする。
  unsigned int x = 1 ;
  // result =



! 演算子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



! 演算子は、オペランドをboolに変換し、その否定を返す。つまり、オペランドがtrueの場合はfalseに、falseの場合はtrueになる。



.. code-block:: c++
  
  !true ; // false
  !false ; // true
  
  int x = 0 ;
  !x ; // 0はfalseに変換される。その否定なので、結果はtrue




~ 演算子
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



~ 演算子は、ビット反転とも呼ばれている。オペランドには、整数型と非scoped enum型が使える。式の結果は、オペランドの1の補数となる。すなわち、オペランドの各ビットが反転された値となる。オペランドには整数のプロモーションが適用される。



.. code-block:: c++
  
  int x = 0 ;
  // ビット列の各ビットを反転する
  ~x ;






インクリメントとデクリメント（Increment and decrement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  ++ 式
  -- 式


ここでは、前置式のインクリメントとデクリメントについて解説する。<a href="#expr.post.incr">後置式のインクリメントとデクリメント</a>も参照。



前置式の++ 演算子は、オペランドに1を加算して、その結果をそのまま返す。オペランドは数値型かポインター型で、変更可能なlvalueでなければならない。式の結果はlvalueになる。



前置式の-- 演算子は、オペランドから1を減算する。それ以外は、++演算子と同じように動く。



.. code-block:: c++
  
  int x = 0 ;
  int result = ++x ;
  // ここで、result = 1, x = 1




sizeof（Sizeof）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  sizeof ( 未評価式 )
  sizeof ( 型名 )
  sizeof ... ( 識別子 )


sizeofとは、オペランドを表現するオブジェクトのバイト数を返す演算子である。オペランドは、未評価式か型名になる。



オペランドに型名を指定した場合、sizeof演算子は、型のオブジェクトのバイト数を返す。sizeof(char)、sizeof(signed char)、sizeof(unsigned char)は、1を返す。それ以外のあらゆる型のサイズは、実装によって定義される。たとえば、sizeof(bool)やsizeof(char16_t)やsizeof(char32_t)のサイズも、規格では決められていない。



.. code-block:: c++
  
  // 1
  sizeof(char) ;
  // int型のオブジェクトのサイズ
  sizeof(int) ;


オペランドに式を指定した場合、その式の結果の型のオブジェクトのバイト数を返す。式は評価されない。<a href="#conv.lval">lvalueからrvalueへの型変換</a>、<a href="#conv.array">配列からポインターへの型変換</a>、<a href="#conv.func">関数からポインターへの型変換</a>は行われない。



.. code-block:: c++
  
  int f() ;
  
  // int型のオブジェクトのサイズ
  sizeof( f() ) ;
  // int型のオブジェクトのサイズ
  sizeof( 1 + 1 ) ;


関数呼び出しの式の結果の型は、関数の戻り値の型になる。



オペランドには、関数と不完全型を使うことはできない。関数は、そもそもオブジェクトではないし、不完全型は、そのサイズを決定できないからだ。「関数」は使えないが、関数呼び出しは「関数」ではないので使える。また、関数ポインターにも使える。



.. code-block:: c++
  
  int f () ;
  struct Incomplete ;
  
  // 関数呼び出しは「関数」ではない
  // sizeof(int) と同じ
  sizeof( f() ) ;
  // 関数ポインターはオブジェクトであるので、使える
  // sizeof ( int (*)(void) ) と同じ
  sizeof( &f ) ;
  
  // エラー、関数を使うことはできない
  sizeof( f ) ;
  // エラー、不完全型を使うことはできない
  sizeof( Incomplete ) ;


オペランドがリファレンス型の場合、参照される型のオブジェクトのサイズになる。



.. code-block:: c++
  
  void f( int & ref )
  {
  // sizeof(int)と同じ
  sizeof(int &) ;
  sizeof(int &&) ;
  sizeof( ref ) ;
  }


オペランドがクラス型の場合、クラスのオブジェクトのバイト数になる。これには、アライメントの調整や、配列の要素として使えるようにするための実装依存のパディングなども含まれる。クラス型のサイズは、必ず1以上になる。これは、サイズが0では、ポインターの演算などに差し支えるからである。



オペランドが配列型の場合、配列のバイト数になる。これはつまり、要素の型のサイズ　×　要素数となる。



.. code-block:: c++
  
  // sizeof(int) * 10 と同じ
  sizeof( int [10] ) ;
  
  char a[10] ;
  // sizeof(char) * 10 = 1 * 10 = 10
  sizeof( a ) ;
  
  // この型は配列ではなく、int
  // sizeof(int)と同じ
  sizeof( a[0] ) ;


sizeof...は、オブジェクトのバイト数とは、何の関係もない。sizeof...のオペランドには、パラメーターパックの識別子を指定できる。sizeof...演算子は、オペランドのパラメーターパックの引数の数を返す。sizeof...演算子の結果は定数で、型はstd::size_tである。



.. code-block:: c++
  
  #include <cstddef>
  #include <iostream>
  
  template < typename... Types >
  void f( Types... args )
  {
      std::size_t const t = sizeof...(Types) ;
      std::size_t const a = sizeof...(args) ;
  
      std::cout << t << ", " << a << std::endl ;    
  }
  
  int main()
  {
      f() ; // 0, 0
      f(1,2,3) ; // 3, 3
      f(1,2,3,4,5) ; // 5, 5
  }




new
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



確保関数と解放関数の具体的な実装方法については、<a href="#support.dynamic">動的メモリー管理</a>を参照。



.. code-block:: c++
  
  

newに必要な宣言の一部は、&lt;new&gt;ヘッダーで定義されているので、使う際は、これをincludeしなければならない。



new式は、型名のオブジェクトを生成する。newされる型は、完全型でなければならない。ただし、抽象クラスはnewできない。リファレンスはオブジェクトではないため、newできない。new式の結果は、型が配列以外の場合は、生成されたオブジェクトへのポインターを返す。型が配列の場合は、配列の先頭要素へのポインターを返す。



.. code-block:: c++
  
  class C {} ;
  int main()
  {
      // int型のオブジェクトを生成する
      int * i = new int ;
      // C型のオブジェクトを生成する
      C * c = new C ;
  }


newが、オブジェクトのためのストレージの確保に失敗した場合、std::bad_alloc例外がthrowされる。



.. code-block:: c++
  
  int main()
  {
      try {
          new int ;
      } catch( std::bad_alloc )
      {
          // newが失敗した
      }
  }


詳細なエラーについては、後述する。



newによって生成されるオブジェクトは、<a href="#basic.stc.dynamic">動的ストレージの有効期間</a>を持つ。つまり、newによって作られたオブジェクトを破棄するためには、明示的にdeleteを使わなければならない。



.. code-block:: c++
  
  int main()
  {
      int * ptr = new int ; // 生成
      delete ptr ; // 破棄
  }


new式の評価
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



new式に、new初期化子が指定されている場合、その式を評価する。次に、確保関数（allocation function）を呼び出して、オブジェクトの生成に必要なストレージを確保する。初期化を行ない、確保したストレージ上に、オブジェクトを構築する。そして、オブジェクトへのポインターを返す。




配列の生成
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



newで配列を生成する場合、要素数は、定数でなくても構わない。



.. code-block:: c++
  
  void f( int n )
  {
      // 5個のint型の配列を生成する
      // 要素数は定数
      new int[5] ;
  
      // n個のint型の配列を生成する
      // 要素数は定数ではない
      new int[n] ;
  }


配列の配列、つまり多次元配列を生成する場合、配列型の最初に指定する要素数は、定数でなくても構わない。残りの要素数は、すべて定数でなければならない。



.. code-block:: c++
  
  void f( int n )
  {
      // 要素数はすべて定数
      new int[5][5][5] ;
  
      // OK
      // 最初の要素数は定数ではない
      // 残りはすべて定数
      new int[n][5][5] ;
  
      new int [n] // 最初の要素数は定数でなくてもよい
              [5][5] ; // 残りの要素数は定数でなければならない
  
      // エラー
      // 最初以外の要素数が定数ではない
      new int[n][n][n] ;
      new int[5][n][n] ;
      new int[5][n][5] ;
  }


配列の要素数が0の場合、newは、0個の配列を生成する。配列の要素数が負数であった場合の挙動は未定義である。



.. code-block:: c++
  
  int main()
  {
      // OK 
      int * ptr = new int[0] ;
      // もちろんdeleteしなければならない
      delete [] ptr ;
  
      // エラー
      new int[-1] ;
  }


もし、配列型の定数ではない要素数が、実装の制限以上の大きさである場合、ストレージの確保は失敗する。その場合、std::bad_array_new_length例外がthrowされる。要素数が定数であった場合は、通常通り、std::bad_alloc例外がthrowされる。



.. code-block:: c++
  
  // int[n]のストレージを確保できないとする。
  int main()
  {
      try {
          std::size_t n = std::numeric_limits<std::size_t>::max() ;
          new int[n] ; // 要素数は定数ではない
      } catch( std::bad_array_new_length )
      {
          // ストレージを確保できなかった場合
      }
  
      try {
          // numeric_limitsのメンバー関数maxはconstexpr関数なので、定数になる。
          std::size_t const n = std::numeric_limits<std::size_t>::max() ;
          new int[n] ;// 要素数は定数
      } catch( std::bad_alloc )
      {
          // ストレージを確保できなかった場合
      }    
  }


要素数が定数でない場合で、ストレージが確保できない場合のみ、std::bad_array_new_lengthがthrowされる。要素数が定数の場合は、通常通り、std::bad_allocがthrowされる。




オブジェクトの初期化
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



生成するオブジェクトの初期化は、new初期化子によって指定される。new初期化子とは、( 式リスト )か、初期化リストのいずれかである。new初期化子が指定された場合、オブジェクトは、直接初期化される。new初期化子が省略された場合、デフォルト初期化される。



.. code-block:: c++
  
  struct C
  {
      C() {}
      C(int) {}
      C(int,int) {}
  } ;
  
  
  int main()
  {
      // new初期化子が省略されている
      // デフォルト初期化
      new C ;
  
      // 直接初期化
      new C(0) ;
      new C(0, 0) ;
  
      // 初期化リスト
      new C{0} ;
      new C{0,0} ;
  }


組み込み型に対するデフォルト初期化は、「初期化しない」という挙動なので、注意を要する。初期化についての詳しい説明は、<a href="#dcl.init">初期化子</a>を参照。




型名としてのauto
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



newの型名がautoの場合、new初期化子は、( 代入式 )の形を取らなければならない。オブジェクトの型は、代入式の結果の型となる。オブジェクトは代入式の結果の値で初期化される。



.. code-block:: c++
  
  int f() { return 0 ; }
  int main()
  {
      // int型、値は0
      new auto( 0 ) ;
      // double型、値は0.0
      new auto( 0.0 ) ;
      // float型、値は0.0f
      new auto( 0.0f ) ;
      // int型、値は関数fの戻り値
      new auto( f() ) ;
  }


これは、auto指定子とよく似ている。




placement new
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



placement newとは、確保関数に追加の引数を渡すことができるnew式の文法である。これは、対応するnew演算子のオーバーロード関数を呼び出す。



.. code-block:: c++
  
  void * operator new( std::size_t size, int ) throw(std::bad_alloc)
  { return operator new(size) ; }
  void * operator new( std::size_t size, int, int ) throw(std::bad_alloc)
  { return operator new(size) ; }
  void * operator new( std::size_t size, int, int, int ) throw(std::bad_alloc)
  { return operator new(size) ; }
  
  int main()
  {
      new(1) int ; // operator new( sizeof(int), 1 )
      new(1,2) int ; // operator new( sizeof(int), 1, 2 )
      new(1,2,3) int ; // operator new( sizeof(int), 1, 2, 3 )
  }


このように、newと型名の間に、通常の関数の実引数のリストのように、追加の引数を指定することができる。追加の引数は、operator newの二番目以降の引数に渡される。placement newの追加の引数は、ストレージを確保する方法を確保関数に指定するなどの用途に使える。




特殊なplacement new
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



C++には、あらかじめplacement newが二つ定義されている。operator new(std::size_t, const std::nothrow_t &amp;) throw()と、operator new(std::size_t, void *) throw()である。



operator new(std::size_t, const std::nothrow_t &amp;) throw()は、ストレージの確保に失敗しても例外を投げない特別な確保関数である。これには通常、std::nothrowが渡される。



.. code-block:: c++
  
  // デフォルトで実装により定義される確保関数
  // void * operator new(std::size_t, const std::nothrow_t &) throw() ;
  
  int main()
  {
      // 失敗しても例外を投げない
      int * ptr = new(std::nothrow) int ;
  
      if ( ptr != nullptr )
      {
          // オブジェクトの生成に成功
          // 参照できる
          *ptr = 0 ;
      }
  
      delete ptr ;
  }


nothrow版のnew演算子のオーバーロードは、ストレージの確保に失敗しても、例外を投げない。かわりに、nullポインターを返す。これは、newは使いたいが、どうしても例外を使いたくない状況で使うことができる。nothrow版のnewを呼び出した場合は、戻り値がnullポインターであるかどうかを確認しなければならない。



std::nothrow_tは、単にオーバーロード解決のためのタグに過ぎない。また、引数として渡しているstd::nothrowは、単に便利な変数である。



.. code-block:: c++
  
  // 実装例
  namespace std {
      struct nothrow_t {} ;
      extern const nothrow_t nothrow ;
  }


operator new(std::size_t, void *) throw()は、非常に特別な確保関数である。この形のnew演算子はオーバーロードできない。このnew演算子は、ストレージを確保する代わりに、第二引数に指定されたポインターの指すストレージ上に、オブジェクトを構築する。第二引数のポインターは、オブジェクトの構築に必要なサイズやアライメント要求などの条件を満たしていなければならない。



一般に、placement newといえば、この特別なnew演算子の呼び出しを意味する。ただし、正式なplacement newという用語の意味は、追加の実引数を指定するnew式の文法である。



.. code-block:: c++
  
  struct C
  {
      C(){ std::cout << "constructed." << std::endl ; }
      ~C(){ std::cout << "destructed." << std::endl ; }
  } ;
  
  int main()
  {
      // ストレージを自前で確保する
      // operator newの返すストレージは、あらゆるアライメント要求を満たす
      void * storage = operator new( sizeof(C) ) ;
  
      // placement newによって、ストレージ上にオブジェクトを構築
      C * ptr = new( storage ) C ;
  
      // ストレージの開放の前に、デストラクターを呼び出す
      ptr->~C() ;
  
      // ストレージを自前で開放する
      operator delete( storage ) ;
  }


ストレージは自前で確保しなければならないので、通常通りdelete式を使うことはできない。デストラクターを自前で呼び出し、その後に、ストレージを自前で解放しなければならない。



ストレージは、動的ストレージでなくても構わない。ただし、アライメント要求には注意しなければならない。



.. code-block:: c++
  
  struct C
  {
      int x ;
      double y ;
  } ;
  
  int main()
  {
      // ストレージは自動変数
      char storage [[align(C)]] [sizeof(C)] ;
  
      // placement newによって、ストレージ上にオブジェクトを構築
      C * ptr = new( storage ) C ;
  
      // デストラクターはtrivialなので呼ぶ必要はない。
      // ストレージは自動変数なので、開放する必要はない
  }


この例では、sizeof(C)の大きさのchar配列の上にオブジェクトを構築している。アトリビュートを使い、アライメントを指定していることに注意。



このplacement newは、STLのアロケーターを実装するのにも使われている。




ストレージの確保に失敗した場合のエラー処理
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



確保関数がストレージの確保に失敗した場合、std::bad_alloc例外がthrowされる。placement newのstd::nothrow_tを引数に取る確保関数の場合は、戻り値のポインターが、nullポインターとなる。



.. code-block:: c++
  
  int main()
  {
      try {
          new int ;
      } catch( std::bad_alloc )
      {
          // エラー処理
      }
  
      int * ptr = new(std::nothrow) int ;
  
      if ( ptr == nullptr )
      {
          // エラー処理
      }
  }




初期化に失敗した場合のエラー処理
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



newが失敗する場合は、二つある。ストレージが確保に失敗した場合と、オブジェクトの初期化に失敗した場合である。



たとえストレージが確保できたとしても、オブジェクトの初期化は、失敗する可能性がある。なぜならば、初期化の際に、コンストラクターが例外を投げるかもしれないからだ。



.. code-block:: c++
  
  // 例外を投げるコンストラクターを持つクラス
  struct Fail
  {
      Fail() { throw 0 ; }
  } ;
  
  int main()
  {
      try {
          new Fail ; // 必ず初期化に失敗する
      } catch( int ) { }
  }


コンストラクターが例外を投げた場合、newは、確保したストレージを、対応する解放関数（deallocation function）を呼び出して解放する。そして、コンストラクターの投げた例外を、そのまま外に伝える。



対応する解放関数とは何か。通常は、operator delete(void *)である。しかし、placement newを使っている場合は、最初の引数を除く、残りの引数の数と型が一致するoperator deleteになる。



.. code-block:: c++
  
  // placement new
  void * operator new( std::size_t size, int, int, int ) throw(std::bad_alloc)
  { return operator new(size) ; }
  
  // placement delete
  void operator delete( void * ptr, int, int, int ) throw()
  {
      std::cout << "placement delete" << std::endl ;
      operator delete(ptr) ;
  }
  
  // 例外を投げるかもしれないクラス
  struct Fail
  {
      Fail() noexcept(false) ; // 例外を投げる可能性がある
  } ;
  
  int main()
  {
      // コンストラクターが例外を投げた場合、
      // operator delete( /*ストレージへのポインター*/, 1, 2, 3 )が呼ばれる
      Fail * ptr = new(1, 2, 3) Fail ;
  
      // operator delete(void *)が呼ばれる
      delete ptr ;
  }


初期化が失敗した場合のplacement deleteの呼び出しには、placement newに渡された追加の引数と、全く同じ値が渡される。



なお、delete式は通常通り、operator delete(void *)を呼び出す。たとえplacement newで確保したオブジェクトであっても、delete式では対応する解放関数は呼ばれない。あくまで、初期化の際に呼ばれるだけである。また、delete式から、placement deleteを呼び出す文法も存在しない。これは、「newの際に指定した情報を、deleteの際にまで保持しておくのは、ユーザー側にとっても実装側にとっても困難である」という思想に基づく。




確保関数の選択
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



new式が呼び出す確保関数は、以下の方法で選択される。



生成するクラスのメンバー関数に、operator newのオーバーロードがある場合、メンバー関数が選ばれる。メンバー関数によってオーバーロードされていない場合、グローバルスコープのoperator newが選ばれる。new式が、「::new」で始まる場合、たとえメンバー関数によるオーバーロードがあっても、グローバルスコープのoperator newが選ばれる



.. code-block:: c++
  
  // オーバーロードあり
  struct A
  {
      void * operator new( std::size_t size ) throw(std::bad_alloc) ;
  } ;
  
  // オーバーロードなし
  struct B { } ;
  
  int main()
  {
      // A::operator newが選ばれる
      new A ;
      // ::operator newが選ばれる
      new B ;
  
      // ::operator newが選ばれる
      ::new A ;
  }


配列の場合も同様である。配列の場合メンバー関数は、配列の要素のクラス型のメンバーから探される。



.. code-block:: c++
  
  // オーバーロードあり
  struct A
  {
      void * operator new[]( std::size_t size ) throw(std::bad_alloc) ;
  } ;
  
  // オーバーロードなし
  struct B { } ;
  
  int main()
  {
      // A::operator new[]が選ばれる
      new A[1] ;
      // ::operator new[]が選ばれる
      new B1[1] ;
  
      // ::operator new[]が選ばれる
      ::new A[1] ;
  }


placement newの場合、追加の引数が、オーバーロード解決によって考慮され、最も最適なオーバーロード関数が選ばれる。



.. code-block:: c++
  
  void * operator new( std::size_t size, int ) throw( std::bad_alloc ) ;
  void * operator new( std::size_t size, double ) throw( std::bad_alloc ) ;
  void * operator new( std::size_t size, int, int ) throw( std::bad_alloc ) ;
  
  int main()
  {
      // operator new( std::size_t size, int )
      new(0) int ;
      // operator new( std::size_t size, double )
      new(0.0) int ;
      // operator new( std::size_t size, int, int )
      new(1, 2) int ;
  }




CV修飾されている型のnew
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



CV修飾子のある型もnewできる。特に変わることはない。



.. code-block:: c++
  
  int main()
  {
      int const * ptr = new int const(0) ;
      delete ptr ;
  }






delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



確保関数と解放関数の具体的な実装方法については、<a href="#support.dynamic">動的メモリー管理</a>を参照。



.. code-block:: c++
  
  

new式によって確保したオブジェクトの寿命は、スコープにはとらわれない。オブジェクトを破棄したければ、delete式で解放しなければならない。



deleteのオペランドの値は、new式によって返されたポインターでなければならない。オブジェクトが配列ではない場合は、deleteを、配列の場合は、delete [ ]を使う。delete式の結果の型は、voidである。



.. code-block:: c++
  
  int main()
  {
      int * ptr = new int ;
      int * array_ptr = new int[1] ;
  
      delete ptr ;
      delete[] array_ptr ;
  }


配列であるかどうかで、deleteとdelete[]を使い分けなければならない。これは間違えやすいので注意すること。



deleteのオペランドがクラスのオブジェクトであった場合、非explicitなユーザー定義の変換が定義されている場合、オブジェクトへのポインターに変換される。



.. code-block:: c++
  
  struct C
  {
      operator int *() { return new int ; }
  } ;
  
  int main()
  {
      C c ;
      // C::operator int *()を呼び出し、
      // 戻り値を解放する。
      delete c ;
  }


delete式は、まず、ポインターの指し示すオブジェクトのデストラクターを呼び出す。次に、解放関数を呼び出して、ストレージを開放する。オブジェクトのの指す型が、メンバー関数としてoperator deleteのオーバーロードを持つ場合、メンバー関数が呼ばれる。オーバーロードされたメンバー関数が存在しない場合、グローバルスコープのoperator deleteを呼び出す。delete式が、「::delete」で始まる場合、メンバー関数のオーバーロードの有無にかかわらず、グローバルスコープのoperator deleteを呼び出す。



.. code-block:: c++
  
  // オーバーロードあり
  struct A
  {
      void operator delete( void * ) throw() ;
  } ;
  
  // オーバーロードなし
  struct B { } ;
  
  int main()
  {
      A * a = new A ;
      // A::operator delete(void*)を呼び出す
      delete a ; 
  
      B * b = new B ;
      // ::operator delete(void*)を呼び出す
      delete b ;
  
      a = new A ;
      // ::operator delete(void*)を呼び出す
      ::delete a ;
  }


オブジェクトが、placement newで確保されたとしても、呼び出す解放関数は、必ずoperator delete(void *)、もしくはoperator delete[](void *)となる。delete式では、placement deleteは呼び出されない。また、delete式には、placement deleteを呼び出すための文法も存在しない。どうしてもplacement deleteを呼び出したい場合は、手動でデストラクターを呼び出し、さらに手動でplacement deleteを呼び出すしかない。



.. code-block:: c++
  
  // placement delete
  void operator delete( void *, int ) throw() ;
  
  struct C
  {
      C() {}
      ~C(){}
  } ;
  
  void f()
  {
      C * ptr = new C ;
  
      // これでは、operator delete( void * )が呼び出される
      delete ptr ;
  
      // 疑似デストラクター呼び出し
      ptr->~C() ;
      // operator deleteの明示的な呼び出し
      operator delete( ptr, 0 ) ;
  }




alignof
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  alignof ( 型名 )


alignof式は、オペランドの型のアライメント要求を返す。オペランドの型は、完全なオブジェクト型か、その配列もしくはリファレンスでなければならない。式の結果は、std::size_t型の定数になる。



オペランドが、リファレンス型の場合、結果は参照される型のアライメント要求になる。配列の場合、結果は配列の要素の型のアライメント要求になる。



.. code-block:: c++
  
  struct C
  {
      char c ; int i ; double d ;
  } ;
  
  void f()
  {
      // char型のアライメント要求を返す
      alignof( char ) ;
      // int型のアライメント要求を返す
      alignof( int ) ;
      // double型のアライメント要求を返す
      alignof( double ) ;
      // C型のアライメント要求を返す
      alignof( C ) ;
  }




noexcept演算子（noexcept operator）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  noexcept ( 未評価式 )


noexcept演算子は、オペランドの式が、例外を投げる可能性のある式を含むかどうかを返す。noexcept演算子の結果の型はboolの定数で、例外を投げる可能性のある式を含まない場合trueを、含む場合falseを返す。オペランドの式は、評価されない。



結果がfalseとなる場合、すなわち、例外を投げる可能性のある式とは、以下の通りである。



throw式。


.. code-block:: c++
  
  // false
  noexcept( throw 0 ) ;


dynamic_cast式、dynamic_cast&lt;T&gt;(v)において、Tがリファレンス型で、実行時チェックが必要な場合。



.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base { } ;
  
  void f( Base & ref )
  {
      // false
      noexcept( dynamic_cast<Derived & >( ref ) ) ;
  }


typeid式において、オペランドがglvalueで、実行時チェックが必要な場合。




.. code-block:: c++
  
  struct Base { virtual void f() {} } ;
  struct Derived : Base { } ;
  
  void f( Base * ptr )
  {
      // false
      noexcept( typeid( *ptr ) ) ;
  }


関数、メンバー関数、関数ポインター、メンバー関数ポインターを呼び出す式において、呼び出す関数の例外指定が、無例外（non-throwing）であるもの。



.. code-block:: c++
  
  void a() ;
  void b() noexcept ; // non-throwing
  void c() noexcept(true) ; // non-throwing
  void d() noexcept(false) ;
  void e() throw() ; // non-throwing
  void f() throw(int) ;
  
  int main()
  {
      noexcept( a() ) ; // false
      noexcept( b() ) ; // true
      noexcept( c() ) ; // true
      noexcept( d() ) ; // false
      noexcept( e() ) ; // true
      noexcept( f() ) ; // false
  }


関数を、「呼び出す式」というのは、関数を間接的に呼び出す場合も該当する。たとえば、new式は確保関数を呼び出すので、関数を呼び出す式である。その場合の結果は、呼び出される確保関数の例外指定に依存する。



.. code-block:: c++
  
  int main()
  {
      // ::operator new( std::size_t ) throw( std::bad_alloc) を呼び出す
      std::cout << noexcept( new int ) ; // false
  
      // ::operator new( std::size_t, std::nothrow_t ) throw() を呼び出す
      std::cout << noexcept( new(std::nothrow) int ) ; // true
  }


もちろん、演算子のオーバーロード関数も、「関数」である。従って、演算子のオーバーロード関数を呼び出す式は、関数を呼び出す式である。



.. code-block:: c++
  
  struct C
  {
      C operator +( C ) ;
      C operator -( C ) noexcept ;
  } ;
  
  
  int main()
  {
      int i = 0 ;
      noexcept( i + i ) ; // true
  
      C c ;
      noexcept( c + c ) ; // false
      noexcept( c - c ) ; // true
  }


その他にも、関数を間接的に呼び出す可能性のある式というのは、非常に多いので、注意しなければならない。



関数のオーバーロード解決は静的に行われるので、当然、呼び出される関数に応じて結果も変わる。



.. code-block:: c++
  
  void f(int) noexcept ;
  void f(double) ;
  
  int main()
  {
      noexcept( f(0) ) ; // true
      noexcept( f(0.0) ) ; // false
  }


例外を投げる可能性のある式を「含む」というのは、たとえその式が絶対に評価されないでも、例外を投げる可能性があるとみなされる。例えば、



.. code-block:: c++
  
  noexcept( true ? 0 : throw 0 ) ; // false


このnoexceptのオペランドの式は、もし評価された場合、決して例外を投げることがない。しかし、例外を投げる可能性のある式を含んでいるので、noexceptの結果はfalseとなる。



上記以外の場合、noexceptの結果はtrueとなる。



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  int main()
  {
      noexcept( 0 ) ; // true
  
      Derived d ;
      noexcept( d ) ; // true
      noexcept( dynamic_cast<Base &>( d ) ) ; // true
      noexcept( typeid( d ) ) ; // true
  }




キャスト形式による明示的型変換（Explicit type conversion (cast notation)）
--------------------------------------------------------------------------------



注意：C形式のキャストには様々な問題があるので、使ってはならない。



.. code-block:: c++
  
  ( 型名 ) 式


これは、悪名高いC形式のキャストである。



.. code-block:: c++
  
  int main()
  {
      int i = 0 ;
      double * ptr = (double *) &i ;
  }


C形式のキャストは、static_castとreinterpret_castとconst_castを組み合わせた働きをする。組み合わせは、以下の順序で決定される。



0 const_cast
1 static_cast
2 static_castとconst_cast
3 reinterpret_cast
4 reinterpret_castとconst_cast


上から下に評価していき、変換できる組み合わせが見つかったところで、そのキャストを使って変換する。



ただし、C形式のキャストでは、static_castに特別な変更を三つ加える。クラスのアクセス指定を無視できる機能である。



 派生クラスへのポインターやリファレンスから、基本クラスへのポインターやリファレンスに変換できる。文字通り変換できる。アクセス指定などは考慮されない。 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : private Base { } ;
  
  int main()
  {
      Derived d ;
  
      Base & ref1 = (Base &) d ; // OK
      Base & ref2 = static_cast<Base &>(d) ; // ill-formed
  }


このため、publicではない基本クラスにアクセスできてしまう。




 派生クラスのメンバーへのポインターから、曖昧ではない非virtualな基本クラスのメンバーへのポインターに変換できる。文字通り変換できる。アクセス指定などは考慮されない。 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : private Base { int x ; } ;
  
  int main()
  {
      int Base::* ptr1 = (int Base::*) &Derived::x ; // OK
      int Base::* ptr2 = static_cast<int Base::*>(&Derived::x) ; // ill-formed
  }


これも、アクセス指定を無視できてしまう。




 曖昧ではなく非virtualな基本クラスのポインターやリファレンスあるいはメンバーへのポインターは、派生クラスのポインターやリファレンスあるいはメンバーへのポインターに変換できる。文字通り変換できる。アクセス指定などは考慮されない。 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  struct Base { int x ; } ;
  struct Derived : private Base { } ;
  
  int main()
  {
      Derived d ;
  
      d.x = 0 ; // ill-formed. アクセス指定のため
  
      int Derived::* ptr = (int Derived::*) &Base::x ; // well-formed.
      d.*ptr = 0 ; // well-formed. C形式のキャストを使ったため、アクセス指定を無視できている
  }




C形式のキャストでしかできないキャストとは、クラスのアクセス指定を無視し、しかもクラス階層のナビゲーションを行うキャストのことである。



これらのキャストは、reinterpret_castでもできる。ただし、reinterpret_castは、クラス階層のナビゲーションを行わないので、正しく動かない。static_castは、クラス階層のナビゲーションを行うので、正しく動く。



アクセス指定を無視できるキャストをしなければならない場合というのは、現実には存在しないはずである。アクセス指定を無視するぐらいならば、最初からpublicにしておけばいい。



reinterpret_castは必要である。C++が必要とされる環境では、ポインターの内部的な値を、そのまま別の型のポインターとして使わなければならない場合も存在する。また、既存のCのコードとの互換性のため、const_castも残念ながら必要である。しかし、アクセス指定は、C++に新しく追加された概念であるので、互換性の問題も存在しないし、また、アクセス指定を無視しなければならない場合というのも、全く考えられない。従って、アクセス指定を無視できるという理由で、C形式のキャストを使ってはならない。



そもそも、C形式のキャストは根本的に邪悪であるので、使ってはならない。C形式のキャストの問題点は、できることが多すぎるということだ。安全なキャストも、危険なキャストも、全く同じ文法で行うことができる。C++では、この問題を解決するために、キャストを三つに分けた。static_cast、reinterpret_cast、const_castである。C++では、この新しい形式のキャストを使うべきである。以下にその概要と簡単な使い分けをまとめる。



<a href="#expr.static.cast">static_cast</a>は、ほとんどが安全なキャストである。static_castは、型変換を安全にするため、値を変えることもある。値を変更するので、static_castは、クラス階層のナビゲーションを行うことができる。派生クラスと基本クラスとの間のポインターの型変換は、ポインターの内部的な値が変わる可能性があるからだ。ポインターの値は、もとより実装依存であるが、最も多くの環境で再現できるコードは、複数の基本クラスを使うものだ。



.. code-block:: c++
  
  struct Base1 { int x ; } ;
  struct Base2 { int x ; } ;
  
  struct Derived : Base1, Base2 { } ;
  
  
  int main()
  {
      Derived d ;
      Derived * ptr = &d ;
  
      // 基本クラスへのキャスト
      Base1 * base1 = static_cast<Base1 *>( ptr ) ;
      Base2 * base2 = static_cast<Base2 *>( ptr ) ;
  
      // 派生クラスへのキャスト
      Derived * d1 = static_cast<Derived *>( base1 ) ;
      Derived * d2 = static_cast<Derived *>( base2 ) ;
  
  
      // 派生クラスのポインターの値
      std::printf( "Derived *: %p\n", ptr ) ;
  
      // 基本クラスのポインターの値は同じか？
      std::printf( "Base1 *: %p\n", base1 ) ;
      std::printf( "Base2 *: %p\n", base2 ) ;
  
      // 派生クラスに戻した場合はどうか？
      std::printf( "from Base1 * to Derived *: %p\n", d1 ) ;
      std::printf( "from Base1 * to Derived *: %p\n", d2 ) ;
  }


複数の基本クラスの場合、基本クラスのサブオブジェクトが複数あるので、派生クラスと基本クラスのポインターの間で、同じ値を使うことができない。従って、基本クラスへのポインターにキャストするには、ストレージ上の、その基本クラスのサブオブジェクトを指すポインターを返さなければならない。また、派生クラスへのポインターにキャストするには、値を戻さなければならない。



このため、クラス階層のナビゲーションには、static_castかdynamic_castを用いなければならない。



<a href="#expr.reinterpret.cast">reinterpret_cast</a>は、危険で愚直なキャストである。reinterpret_castは、値を変えない。ただ、その値の型だけを変更する。reinterpret_castは、クラス階層のナビゲーションができない。



<a href="#expr.const.cast">const_cast</a>は、CV修飾子を外すキャストである。



もし、どのキャストを使うべきなのか判断できない場合は、まずstatic_castを使っておけば問題はない。もし、static_castが失敗した場合、本当にそのキャストは安全なのかということを確かめてから、reinterpret_castを使うべきである。const_castは、既存のCのコードの利用以外に使ってはならない。


メンバーへのポインター演算子（Pointer-to-member operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 .* 式
  式 ->* 式


メンバーへのポインター演算子は、「左から右」に評価される。



メンバーへのポインター演算子は、クラスのメンバーへのポインターを使って、クラスのオブジェクトのメンバーにアクセスするための演算子である。クラスのメンバーへのポインターを参照するためには、参照するクラスのオブジェクトが必要である。



.*演算子の第一オペランドには、クラスのオブジェクトを指定する。-&gt;*演算子の第一オペランドには、クラスへのポインターを指定する。第二オペランドには、クラスのメンバーへのポインターを指定する。



.. code-block:: c++
  
  struct C
  {
      int member ;
  } ;
  
  int main()
  {
      int C::* mem_ptr = &C::member ;
  
      C c ;
      c.*mem_ptr = 0 ;
  
      C * ptr = &c ;
      ptr->*mem_ptr = 0 ;
  }


メンバー関数の呼び出しの際は、演算子の優先順位に気をつけなければならない。



.. code-block:: c++
  
  struct C
  {
      void member() {} 
  } ;
  
  int main()
  {
      void (C::* mem_ptr)() = &C::member ;
  
      C c ;
      (c.*mem_ptr)() ;
  
      C * ptr = &c ;
      (ptr->*mem_ptr)() ;
  }


なぜならば、メンバーへのポインター演算子の式より、関数呼び出し式の優先順位の方が高いので、c.*mem_ptr()という式は、c.*( mem_ptr() )という式に解釈されてしまう。これは、mem_ptrという名前に対して、関数呼び出し式を適用した後、その結果を、クラスのメンバーへのポインターとして使う式である。このように解釈されることを避けるために、括弧式を使わなければならない。



その他の細かいルールについては、<a href="#expr.ref">クラスメンバーアクセス</a>と同じである。


乗除算の演算子（Multiplicative operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 * 式
  式 / 式
  式 % 式


乗除算の演算子は、「左から右」に評価される



*演算子と/演算子のオペランドは、数値型かunscoped enum型でなければならない。%演算子のオペランドは、整数型かunscoped enum型でなければならない。オペランドには、通常通り数値に関する標準型変換が適用される。<a href="#expr">式</a>を参照。



*演算子は、乗算を意味する。



/演算子は、除算を意味する。%演算子は、第一オペランドを第二オペランドで割った余りを意味する。第二オペランドの値が0の場合の挙動は未定義である。/演算子の結果の型が整数の場合、小数部分は切り捨てられる。



.. code-block:: c++
  
  int main()
  {
      2 * 3 ; // 6
      10 / 5 ; // 2
      3 % 2 ; // 1
  
      3 / 2 ; // 結果は整数型、小数部分が切り捨てられるので、結果は1
  
      3.0 / 2.0 ; // 結果は浮動小数点数型の1.5
  }


以下は間違っている例である。



.. code-block:: c++
  
  // このコードは間違っている例
  int main()
  {
      // ゼロ除算
      1 / 0 ;
  
      // %演算子のオペランドに浮動小数点数型は使えない
      3.0 % 2.0 ;
  }


加減算の演算子（Additive operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 + 式
  式 - 式


加減算の演算子は、「左から右」に評価される。



両方のオペランドが数値型の場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



+演算子は、加算を意味する。-演算子は、減算を意味する。-演算子の減算とは、第二オペランドの値を第一オペランドから引くことである。結果の型には、通常通り数値型に関する標準型変換が行われる。



.. code-block:: c++
  
  int main()
  {
      1 + 1 ; // 2
      1 - 1 ; // 0
  }




オペランドがポインター型の場合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



まず、ポインターの型は、完全に定義されたオブジェクトでなければならない。ポインターは、配列の要素を指し示しているものとみなされる。たとえ実際には配列の要素を差していないとしても、配列の要素を指しているものとみなされる。



+演算子の片方のオペランドがポインター型の場合、もう片方は、整数型でなければならない。-演算子は、両方のオペランドが同じポインター型か、左オペランドがポインター型で右オペランドが整数型でなければならない。



.. code-block:: c++
  
  int main()
  {
      int array[3] ;
      int * ptr = &array[1] ;
  
      // OK
      ptr + 1 ;
      1 + ptr ;
      ptr + (-1) ;
      (-1) + ptr ;
      ptr - ptr ;
      ptr - 1 ;
      ptr - (-1) ;
  
      // エラー
      ptr + ptr ; // +演算子の両オペランドがポインターとなっている
      1 - ptr ; // -演算子の左オペランドが整数で右オペランドがポインターとなっている
  }


ポインターと整数の加減算の結果の型は、ポインターの型である。結果の値は、ポインターが指す要素に対する配列中の添字に、整数を加減算した要素を指すものとなる。もし、ポインターが配列の添字でi番目の要素を指し示している場合、このポインターに整数nを加算することは、i + n番目の要素を指し示すことになる。同様にして、整数nを減算することは、i - n番目の要素を指し示すことになる。



.. code-block:: c++
  
  int main()
  {
      int array[10] ;
      int * ptr = &array[5] ;
  
      ptr + 2 ; // &array[5 + 2]と同じ
      ptr - 2 ; // &array[5 - 2]と同じ
  }


もし、ポインターが、配列の最後の要素を指している場合、これに1を加えると、結果のポインターは配列の最後の要素のひとつ後ろを指すことになる。ポインターが配列の最後の要素のひとつ後ろを指している場合、これから1を引くと、結果のポインターは配列の最後の要素を指すことになる。



.. code-block:: c++
  
  int main()
  {
      int array[10] ;
      // 配列の最後の要素を指す
      int * ptr = &array[9] ;
  
      // 配列の最後の要素のひとつ後ろを指す
      int * one_past_the_last = ptr + 1 ;
      // 配列の最後の要素を指す
      int * last = one_past_the_last - 1 ;
  }


配列の最後の要素を指しているポインターに1を加算して、最後の要素の一つ後の要素を指すようにしても、規格上、ポインターの値のオーバーフローは起こらないと保証されている。2つ目以降の要素を指し示した場合、挙動は未定義である。



.. code-block:: c++
  
  int main()
  {
      int a[1] ;
      int * p1 = &a[0] ; // 最後の要素
  
      int * p2 = p1 + 1 ; // OK、最後の一つ後の要素
      int * p3 = p2 + 1 ; // 挙動は未定義 
  }


上の例で、もし、ポインターp2を参照した場合、挙動は未定義だが、p2自体は未定義ではない。p3は未定義である。



ポインター同士を減算した場合、結果は、ポインターの指す配列の添字の差になる。ポインターPが配列の添字でi番目の要素を差しており、ポインターQが配列の添字でj番目の要素を指している場合、P - Qは、i - jとなる。配列の添字は、0から始まることに注意。両方のポインターが同じ配列上の要素を差していない場合、挙動は未定義である。



.. code-block:: c++
  
  int main()
  {
      int array[10] ;
      int * P = &array[2] ;
      int * Q = &array[7] ;
  
      P - Q ; // 2 - 7 = -5
      Q - P ; // 7 - 2 = 5
  }


ポインター同士の減算の結果の型は、実装依存であるが、&lt;cstddef&gt;ヘッダーで定義されている、std::ptrdiff_tと同じ型になる。



0という値が、ポインターに足し引きされた場合、結果は、そのポインターの値になる。



.. code-block:: c++
  
  void f( int * ptr )
  {
      ptr == ptr + 0 ; // true
      ptr == ptr - 0 ; // true
  }




シフト演算子（Shift operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 << 式
  式 >> 式


シフト演算子のオペランドは、整数型かunscoped enum型でなければならない。オペランドには、整数のプロモーションが行われる。結果の型は、整数のプロモーションが行われた後のオペランドの型になる。



左シフト、E1 &lt;&lt; E2の結果は、E1をE2ビット、左にシフトしたものとなる。シフトされた後のビットは、0で埋められる。もし、E1の型がunsignedならば、結果の値は、E1 × 2<sup>E2</sup>を、E1の最大値+1で剰余したものとなる。



.. code-block:: c++
  
  // コメント内の値は2進数である。
  int main()
  {
      // 1101
      unsigned int bits = 9 ;
  
      bits << 1 ; // 11010
      bits << 2 ; // 110100
  }


E1の型がsignedの場合、E1が負数でなく、E1 × 2<sup>E2</sup>が表現可能であれば、その値になる。その他の場合は未定義である。これは、signedな整数型の内部表現が2の補数であるとは保証していないので、このようになっている。




.. code-block:: c++
  
  // コメント内の値は2進数である
  int main()
  {
      // 1101
      int bits = 9 ;
  
      bits << 1 ; // 11010
      bits << 2 ; // 110100
  
      -1 << 1 ; // 結果は未定義
  }


右シフト、E1 &gt;&gt; E2の結果は、E1をE2ビット、右にシフトしたものとなる。もし、E1の型がunsignedか、signedで正の数ならば、結果の値は、E1 ÷ 2<sup>E2</sup>の整数部分になる。



.. code-block:: c++
  
  // コメント内の値は2進数である
  int main()
  {
      // 1101
      unsigned int value = 9 ;
  
      value >> 1 ; // 110
      value >> 2 ; // 11
  
      int signed_value = 9 ;
  
      signed_value >> 1 ; // 110
      signed_value >> 2 ; // 11
  }


E1の型がsignedで、値が負数の場合、挙動は未定義である。



.. code-block:: c++
  
  int main()
  {
      -1 >> 1 ; // 結果は未定義
  }


右オペランドの値が負数であったり、整数のプローモーション後の左オペランドのビット数以上の場合の挙動は未定義である。



.. code-block:: c++
  
  // この環境では、1バイトは8ビット
  // sizeof(unsigned int)は2とする。
  // すなわち、この環境では、unsigned intは16ビットとなる。
  int main()
  {
      unsigned int value = 1 ;
      value << -1 ; // 未定義
      value >> -1 ; // 未定義
  
      value << 16 ; // 未定義
      value >> 16 ; // 未定義
  
      value << 17 ; // 未定義
      value >> 17 ; // 未定義
  }


シフト演算には、未定義の部分が非常に多い。ただし、多くの現実の環境では、何らかの具体的な意味が定義されていて、時として、そのような未定義の挙動に依存したコードを書かなければならない場合がある。その場合、特定の環境に依存したコードだという正しい認識を持たなければならない。


関係演算子（Relational operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 < 式
  式 > 式
  式 <= 式
  式 >= 式


関係演算子は「左から右」に評価される。



関係演算子のオペランドには、数値型、enum型、ポインター型を使うことができる。各演算子の意味は、以下のようになっている。



A < B
  AはBより小さい
A > B
  AはBより大きい
A <= B
  AはBより小さいか、等しい
A >= B
  AはBより大きいか、等しい


結果の型はboolとなる。両オペランドが数値型かenum型の場合、不等号の関係が正しければtrueを、そうでなければfalseを返す。



.. code-block:: c++
  
  void f( int a, int b )
  {
      a < b ;
      a > b ;
      a <= b ;
      a >= b ;
  }


式の結果の型はboolである。



ポインター同士の比較に関しては、未規定な部分が多い。ここでは、規格により保証されていることだけを説明する。



同じ型の二つのポインター、pとqが、同じオブジェクトか関数を指している場合、もしくは、配列の最後の要素のひとつ後の要素を指している場合、もしくは、両方ともnullの場合は、p&lt;=qとp&gt;=qhはtrueとなり、p&lt;qとp&gt;qはfalseとなる。



.. code-block:: c++
  
  int main()
  {
      int object = 0 ;
      int * p = &object ;
      int * q = &object ;
  
      p <= q ; // true
      p >= q ; // true
  
      p < q ; // false
      p > q ; // false
  }


同じ型の二つのポインター、pとqが、異なるオブジェクトを差しており、そのオブジェクトは同じオブジェクトのメンバーではなく、また同じ配列内の要素ではなく、異なる関数でもなく、あるいは、どちらか片方の値のみがnullの場合、p&lt;q, p&gt;q, p&lt;=q, p&gt;=qの結果は、未規定である。



.. code-block:: c++
  
  int main()
  {
      int object1 ;
      int object2 ;
  
      int * p = &object1 ;
      int * q = &object2 ;
  
      p <= q ; // 結果は未規定
      p >= q ; // 結果は未規定
  
      p < q ; // 結果は未規定
      p > q ; // 結果は未規定
  
      p < nullptr ; // 結果は未規定
  }


同じ型の二つのポインター、pとqが、同じ配列の要素を指している場合、添字の大きい要素の方が、より大きいと評価される。



.. code-block:: c++
  
  int main()
  {
      int array[2] ;
  
      int * p = &array[0] ;
      int * q = &array[1] ;
  
      p < q ; // true
      p > q ; // false
  
      p <= q ; // true
      p >= q ; // false
  


これと同様に、pとqが指しているものが、同じ型の同じクラスのオブジェクトのサブオブジェクトである場合は、同じアクセスコントロール化にある場合、後に宣言されたメンバーの方が、ポインター同士の比較演算では、大きいと評価される。



.. code-block:: c++
  
  struct S
  {
  // 同じアクセスコントロール下
      int a ;
      int b ; // bが後に宣言されている
  } ;
  
  int main()
  {
      S object ;
      // 同じオブジェクトのサブオブジェクト
      int * p = &object.a ;
      int * q = &object.b ;
  
      p < q ; // true
      p > q ; // false
  } ;


これと似ているが、ただしクラスのメンバーのアクセスコントロールが異なる場合、結果は未規定である。



.. code-block:: c++
  
  struct S
  {
  public :
      int a ;
  private :
      int b ;
  
      void f()
      {
          &a < &b ; // 結果は未規定
      }
  } ;


二つのポインター、pとqが、unionの同じオブジェクトの非staticなデータメンバーを指している場合、等しいと評価される。



.. code-block:: c++
  
  union Object
  {
      int x ;
      int y ;
  } ;
  
  int main()
  {
      Object object ;
      int * p = &object.x ;
      int * q = &object.y ;
  
      p < q ; // false
      p > q ; // false
  
      p <= q ; // true
      p >= q ; // true
  
      p == q ; // true
  }


二つのポインターが、同じ配列内の要素を指している場合、添字の大きい要素を指すポインターのが、大きいと評価される。また、これはどちらか片方のポインターが、配列の範囲を超えていても、評価できる。



.. code-block:: c++
  
  int main()
  {
      int a[2] ;
      int * p1 = &a[0] ;
      int * p2 = &a[1] ;
  
      p1 < p2 ; // true
  
      int * p3 = p2 + 1 ; // p3は配列の範囲外を指す
  
      p1 < p3 ; // OK、結果はtrue
  }


voidへのポインター型は、比較することができる。また、片方のオペランドがvoidへのポインター型で、もう片方が別のポインター型である場合、もう片方のオペランドが、標準型変換によってvoidへのポインター型に変換されるので、比較することができる。もし、両方のポインターが、同じアドレスであった場合かnullポインターの場合は、等しいと評価される。それ以外は、未規定である。



.. code-block:: c++
  
  int main()
  {
      int object = 0 ;
  
      int * ptr = &object ;
      void * p = ptr ;
      void * q = ptr ;
  
      p < q ; // false
      p > q ; // false
  
      p <= q ; // true
      p >= q ; // true
  
      // 標準型変換によって、別のポインター型とも比較できる
      p <= ptr ; // true    
  }


これ以外の比較の結果は、すべて未規定となっている。未定義ではなく、未規定なので、実装によっては、意味のある結果を返すこともある。しかし、実装に依存する挙動なので、移植性に欠ける。


等価演算子（Equality operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 == 式
  式 != 式


==演算子（等しい）と、!=演算子（等しくない）は、<a href="#expr.rel">関係演算子</a>とオペランドや結果の型、評価の方法は同じである。ただし比較の意味は、「等しい」か、「等しくない」かである。



.. code-block:: c++
  
  int main()
  {
      1 == 1 ; // true
      1 != 1 ; // false
  
      1 == 2 ; // false
      1 != 2 ; // true
  }


同じ型のポインターの場合、ともにアドレスが同じか、ともにnullポインターの場合、trueと評価される。




==演算子は、代入演算子である=演算子と間違えやすいので、注意しなければならない。



.. code-block:: c++
  
  void f( int x )
  {
      if ( x = 1 ) // 間違い
      {
          // 処理
      } else {
          // 処理
      }
  }


この例では、if文の条件式の結果は、代入式の結果となってしまう。それは、1であるので、このif文は常にtrueであると評価されてしまう。


ビット列論理積演算子（Bitwise AND operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 & 式


ビット列論理積演算子は、両オペランドの各ビットごとの論理積（AND）を返す。オペランドは整数型か、unscoped enum型でなければならない。


ビット列排他的論理和演算子（Bitwise exclusive OR operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 ^ 式


ビット列排他的論理和演算子は、両オペランドの各ビットごとの排他的論理和（exclusive OR）を返す。オペランドは整数型か、unscoped enum型でなければならない。


ビット列論理和演算子（Bitwise inclusive OR operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 | 式


ビット列論理和演算子は、両オペランドの各ビットごとの論理和（inclusive OR）を返す。オペランドは整数型か、unscoped enum型でなければならない。


論理積演算子（Logical AND operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 && 式


&amp;&amp;演算子は「左から右」に評価される。



論理積演算子は、オペランドの論理積を返す演算子である。両オペランドはboolに変換される。結果の型はboolである。両方のオペランドがtrueであれば、結果はtrue。それ以外はfalseとなる。



.. code-block:: c++
  
  true && true ; // true
  true && false ; // false
  false && true ; // false
  false && false ; // false


第一オペランドを評価した結果がfalseの場合、第二オペランドは評価されない。なぜならば、第一オペランドがfalseであれば、第二オペランドを評価するまでもなく、結果はfalseであると決定できるからである。



.. code-block:: c++
  
  bool f() { return false ; }
  bool g() { return true ; }
  
  int main()
  {
      // g()は呼ばれない。結果はfalse
      f() && g() ;
  }


この例では、第一オペランドである関数fの呼び出しはfalseを返すので、第二オペランドの関数gの呼び出しが評価されることはない。つまり、関数gは呼ばれない。



第二オペランドが評価される時、第一オペランドの評価によって生じた値の計算や副作用は、すべて行われている。



.. code-block:: c++
  
  int main()
  {
      int value = 0 ;
  
      ++value // 値は1になるので、trueと評価される
          &&
      value ; // 値はすでに1となっているので、trueと評価される
  }


論理和演算子（Logical OR operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 || 式


||演算子は、「左から右」に評価される。



論理和演算子は、オペランドの論理和を返す演算子である。両オペランドはboolに変換される。結果の型はboolである。オペランドが片方でもtrueと評価される場合、結果はtrueとなる。両オペランドがfalseの場合に、結果はfalseとなる。



.. code-block:: c++
  
  int main()
  {
      true || true ; // true
      true || false ; // true
      false || true ; // true
      false || false ; // false
  }


第一オペランドを評価した結果がtrueの場合、第二オペランドは評価されない。なぜならば、第一オペランドがtrueであれば、第二オペランドを評価するまでもなく、結果はtrueとなるからである。



.. code-block:: c++
  
  bool f() { return true ; }
  bool g() { return false ; }
  
  int main()
  {
      // g()は呼ばれない。結果はtrue
      f() && g() ;
  }


論理積と同じように、第二オペランドが評価される場合、第一オペランドの評価によって生じた値の計算や副作用は、すべて行われている。


条件演算子（Conditional operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 ? 式 : 代入式


条件演算子は「左から右」に評価される。



条件演算子は、三つのオペランドを取る。C++には他に三つのオペランドを取る演算子がないことから、三項演算子といえば、条件演算子の代名詞のように使われている。しかし、正式名称は条件式であり、演算子の名称は条件演算子である。



条件演算子の第一オペランドはboolに変換される。値がtrueであれば、第二オペランドの式が評価され、その結果が返される。値がfalseであれば、第三オペランドの式が評価され、その結果が返される。第二オペランドと第三オペランドは、どちらか片方しか評価されない。



.. code-block:: c++
  
  bool cond() ;
  int e1() ;
  int e2() ;
  
  int main()
  {
      true ? 1 : 2 ; // 1
      false ? 1 : 2 ; // 2
  
      // 関数condの戻り値によって、関数e1、あるいはe2が呼ばれ、その戻り値が返される。
      // e1とe2は、どちらか片方しか呼ばれない。
      cond() ? e1() : e2() ;
  }


実は、条件演算子は見た目ほど簡単ではない。特に、結果の型をどのようにして決定するかということが、非常に難しい。ここでは、結果の型を決定する完全な詳細は説明しないが、特に重要だと思われる事を取りあげる。



条件演算子の第二第三オペランドには、結果がvoid型となる式を使うことができる。



.. code-block:: c++
  
  void f() {}
  
  int main()
  {
      true ? f() : f() ;
  
      int * ptr = new int ;
      true ? delete ptr : delete ptr ;
  
      true ? throw 0 : throw 0 ;
  }


片方のオペランドがvoidで、もう片方がvoidではない場合、エラーである。



.. code-block:: c++
  
  void f() {}
  int main()
  {
      true ? 0 : f() ; // エラー
      true ? f() : 0 ; // エラー
  }


ただし、片方のオペランドがthrow式の場合に限り、もう片方のオペランドに、voidではない式を使うことができる。もう片方のオペランドがvoid型の場合はエラーとなる。結果はprvalueの値で、型はvoidではない式の型になる。



.. code-block:: c++
  
  void f() {}
  
  int main()
  {
      // OK
      // xに0を代入する
      int x = true ? 0 : throw 0 ;
  
      // エラー
      // 戻り値に123を代入しようとしているが、prvalueには代入できない
      (true ? x : throw 0) = 123 ;
  
      true ? throw 0 : f() ; // エラー
  }


両オペランドが、ともに同じ値カテゴリーで、同じ型の場合は、条件演算子の結果は、その値カテゴリーと型になる。



.. code-block:: c++
  
  int f() { return 0 ; }
  
  int main()
  {
      int x = 0 ;
  
      // 両オペランドとも、lvalueのint型
      // 結果はlvalueのint
      ( true ? x : x ) = 0 ; // lvalueなので代入も可能
  
      // 両オペランドとも、xvalueのint型
      // 結果はxvalueのint
      true ? std::move(x) : std::move(x) ;
  
      // 両オペランドとも、prvalueのint型
      // 結果はprvalueのint
      true ? f() : f() ;
  }


もし、オペランドの値カテゴリーや型が違う場合、暗黙の型変換によって、お互いの型と値カテゴリーを一致させようという試みがなされる。この変換の詳細は、非常に複雑で、通常は意識する必要はないため、本書では省略する。


代入と複合代入演算子（Assignment and compound assignment operators）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  

代入演算子（=）と、複合代入演算子は、「右から左」に評価される。



代入演算子は、左側のオペランドに、右側のオペランドの値を代入する。左側のオペランドは変更可能なlvalueでなければならない。結果として、左側のオペランドのlvalueを返す。



.. code-block:: c++
  
  int main()
  {
      int x ;
      x = 0 ;
  }


初期化と混同しないように注意。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ; // これは初期化
      x = 0 ; // これは代入
  }


=を代入演算子といい、その他の演算子を、複合代入演算子という。



クラスの代入に関する詳細は、<a href="#class.copy">クラスオブジェクトのコピーとムーブ</a>や、オーバーロードの<a href="#over.ass">代入</a>を参照。



複合代入演算子の式、E1 op = E2は、E1 = E1 op E2と同じである。ただし、E1という式は、一度しか評価されない。opには、任意の複合代入演算子の一部が入る。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  
      x += 1 ; // x = x + 1と同じ
      x *= 2 ; // x = x * 2と同じ
  }


右側のオペランドには、初期化リストを使うことができる。



左側のオペランドがスカラー型の場合、ある型Tの変数をxとすると、x = {v}という式は、x = T(v)という式と同じ意味になる。ただし、初期化リストなので、縮小変換は禁止されている。x = {}という式は、x = T()という式と同じ意味になる。



.. code-block:: c++
  
  int main()
  {
      int x ;
      x = {1} ; // x = int(1) と同じ
      x = {} ; // x = int()と同じ
      short s ;
      s = {x} ; // エラー、縮小変換は禁止されている。
  }


それ以外の場合は、初期化リストを実引数として、ユーザー定義の代入演算子が呼び出される。



.. code-block:: c++
  
  struct C
  {
      C(){}
      C( std::initializer_list<int> ) {}
  } ;
  
  int main()
  {
      C c ;
      c = { 1, 2, 3 } ;
  }


コンマ演算子（Comma operator）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  式 , 式


コンマ演算子は、「左から右」に評価される。



コンマ演算子は、まず左のオペランドの式が評価され、次に、右のオペランドの式が評価される。左のオペランドの式を評価した結果は破棄され、右のオペランドの結果が、コンマ演算子の結果として、そのまま返される。結果の型や値、値カテゴリーは、右のオペランドの式を評価した結果と全くおなじになる。



.. code-block:: c++
  
  int main()
  {
      1, 2 ; // 2
      1, 2, 3, 4, 5 ; // 5
  }


右のオペランドの式が評価される前に、左のオペランドの式の値計算や副作用は、すでに行われている。



.. code-block:: c++
  
  int f() ;
  int g() ;
  
  int main()
  {
      int i = 0 ;
      // 左のオペランドのiは、すでにインクリメントされている。
      ++i, i ;
      // 関数gが呼ばれる前に、関数fはすでに呼ばれ終わっている。
      f() , g() ;    
  }


コンマが特別な意味を持つ場面では、コンマ演算子を使うには、明示的に括弧で囲まなければならない。コンマが特別な意味を持つ場面には、例えば、関数の実引数リストや、初期化リストなどがある。



.. code-block:: c++
  
  void f(int, int, int) {}
  int main()
  {
      int x ;
      // 括弧が必要
      f( 1, (x=0, x), 2) ;
  }


この例では、関数fは三つの引数を取る。二つめの引数は、括弧式に囲まれたコンマ演算子の式である。これは変数xに0を代入した後、そのxを引数として渡している。


定数式（Constant expressions）
--------------------------------------------------------------------------------



定数式（constant expression）とは、値がコンパイル時に決定できる式のことである。定数式かどうかということは、C++のいくつかの場面で、重要になってくる。例えば、配列を宣言する時、要素数は定数式でなければならない。



.. code-block:: c++
  
  int main()
  {
      // 整数リテラルは定数式
      int a[5] ;
  
      // const修飾されていて、初期化式が定数式であるオブジェクトは定数式
      int const n = 5 ;
      int b[n] ; // OK
  
      int m = 5 ; // これは定数式ではない
      int c[m] ; // エラー
  }


定数式ではない式
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下に列挙する式は、定数式ではない式である。これらの式を含む式は、その値をコンパイル時に決定することができないので、定数式にはならない。



TODO: constant expressionとconstexpr specifierについては、まだ議論が多く、変更される可能性があるため、執筆を保留。


