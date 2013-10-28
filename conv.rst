標準型変換（Standard conversions）
================================================================================

lvalueからrvalueへの型変換（Lvalue-to-rvalue conversion）
--------------------------------------------------------------------------------



本書では、煩雑を避けるために省略しているが、多くの標準型変換は、ある型のprvalueの値を、別の型のprvalueの値に変換するようになっている。そのため、標準型変換の際には、必要な場合、glvalueが、自動的にprvalueに変換される。これを、lvalueからrvalueへの型変換という。変換できるglvalueは、関数と配列以外である。



この変換は、通常、まず意識することがない。


配列からポインターへの型変換（Array-to-pointer conversion）
--------------------------------------------------------------------------------



配列とポインターは、よく混同される。その理由の一つに、配列名が、あたかもポインターのように振舞うということがある。



.. code-block:: c++
  
  int a[10] ;
  // pは、aの先頭要素を指す。
  int * p = a ;
  
  // どちらも、配列aの先頭要素に0を代入する
  *a = 0 ;
  *p = 0 ;


これは、配列からポインターへの型変換によるものである。配列名は、配列の先頭要素へのポインターとして扱われる。



.. code-block:: c++
  
  int a[10] ;
  
  
  int * p1 = a ; // &a[0]と同じ
  int (* p2 )[10] = &a ; // int [10]へのポインター


ここで、変数aの型は、int [10]であって、int *ではない。ただし、int *に暗黙のうちに型変換されるので、あたかもポインターのように振舞う



多くの人は、これを暗黙の型変換としては意識していない。配列からポインターへの型変換は、非常によく使われる変換であって、多くの式では、配列名は、自動的に、配列の先頭要素へのポインターに型変換される。


関数からポインターへの型変換（Function-to-pointer conversion）
--------------------------------------------------------------------------------



関数の名前は、その関数へのポインターに型変換される。



.. code-block:: c++
  
  void f( void ) {}
  
  int main()
  {
      // typeは関数ポインターの型
      using type = void (*) (void) ;
  
      // 同じ意味。
      type p1 = f ;
      type p2 = &f ;
  }


fの型は、関数であって、関数ポインターではない。関数ポインターとは、&amp;fである。しかし、関数は、暗黙のうちに、関数ポインターに型変換されるので、関数名fは、関数ポインターとしても使うことができる



この型変換も、非常によく使われる。多くの場合は、自動的に、関数は関数ポインターに変換される。



ただし、この型変換は、非staticなメンバー関数には適用されない。ただし、staticなメンバー関数は、この標準変換が適用される。



.. code-block:: c++
  
  struct C
  {
  
      void f(void) {}
      static void g(void) {}
  } ;
  
  // エラー
  void ( C:: * error )(void) = C::f ;
  // OK
  void ( C::* ok )(void) = &C::f ;
  
  // staticなメンバー関数は、普通の関数と同じように、変換できる
  void (*ptr)(void) = C::g ;
  void (*ptr2)(void) = &C::g ; // ただし、こちらの方が分かりやすい


このような暗黙の型変換があるとはいえ、通常、関数ポインターを扱う際には、明示的に<a href="#expr.unary.op">単項演算子</a>である&amp;演算子を使ったほうが、分かりやすい。


CV修飾子の型変換（Qualification conversions）
--------------------------------------------------------------------------------



ある型Tへのポインターは、あるconstまたはvolatile付きの型Tへのポインターに変換できる。



.. code-block:: c++
  
  int * p ;
  int const * cp = p ;
  int volatile * vp = p ;
  int const volatile * cvp = p ;
  
  cvp = cp ;
  cvp = vp ;


これは、より少ないCV修飾子へのポインターから、より多いCV修飾子へのポインターに、暗黙のうちに型変換できるということである。



ただし、ポインターのポインターの場合は、注意を要する。



.. code-block:: c++
  
  int ** p ;
  
  // エラー
  int const ** cp = p ;
  
  // これはOK
  int const * const * cp = p ;


なぜか。実は、この型変換を認めてしまうと、const性に穴が空いてしまうのだ。



.. code-block:: c++
  
  int main()
  {
      int const x = 0 ;
      int * p ;
  
      // これはエラー。
      p = &x ;
  
      // もしこれが認められていたとする。
      // 実際はエラー。
      int const ** cpp = &p ;
  
      // cppを経由して、pを書き換えることができてしまう。
      *cpp = &x ;
  
      // pは、xを参照できてしまう。
      *p = 0 ;
  }


このため、ある型をTとした場合、T **から、T const **への型変換は、認められていない。T **から、T const * const *への変換はできる。



.. code-block:: c++
  
  int * p = nullptr ; 
  int const * const * p2 = &p ; // OK


整数の変換順位（Integer conversion rank）
--------------------------------------------------------------------------------



整数型には、変換順位というものが存在する。これは、標準型変換や、リスト初期化で考慮される、整数型の優先順位である。これは、それほど複雑な順位ではない。基本的には、型のサイズの大小によって決定される。もっとも、多くの場合、型のサイズというのは、実装依存なのだが。



基本的な変換順位は、以下のようになる。



.. code-block:: c++
  
  signed char < short int < int < long int < long long int


unsignedな整数型の順位は、対応するsingedな型と同じである。



この他にも、いくつか細かいルールがある。



charとsigned charと、unsigned charは、同じ順位である。



boolは、最も低い順位となる。



char16_t、char32_t、wchar_tの順位は、実装が割り当てる内部的な型に依存する。従って、これらの変換順位は、実装依存である。



拡張整数型、つまり、実装が独自に定義する整数型は、実装依存の順位になる。


整数のプロモーション（Integral promotions）
--------------------------------------------------------------------------------



整数のプロモーションとは、変換順位の低い型から、高い型へ、型変換することである。ただし、単に順位が低い型から高い型への型変換なら、何でもいいというわけではない。



bool, char16_t, char32_t、wchar_t以外の整数型で、intより変換順位の低い整数型、つまり、char、short、その他の実装独自の拡張整数型は、もし、int型が、その値をすべて表現できる場合、intに変換できる。



.. code-block:: c++
  
  short s = 0 ;
  int i = s ; // 整数のプロモーション
  long l = s ; // これは、整数の型変換


intより低い順位の整数型から、int型への変換ということに注意しなければならない。longやlong longへの変換、または、charからshortへの変換などは、プロモーションではなく、<a href="#conv.integral">整数の型変換</a>に分類される。



char16_t、char32_t、wchar_tは、実装の都合による内部的な整数型に変換できる。内部的な整数型というのは、int、unsigned int、long int、unsigned long int、long long int、unsigned long long intのいずれかである。もし、これらのどの型でも、すべての値を表現できないならば、実装依存の整数型に変換することができる。



今、int型で、char16_tとchar32_tの取りうるすべての値が表現できるものとすると、



.. code-block:: c++
  
  char16_t c16 = u'あ' ;
  char32_t c32 = U'あ' ;
  wchar_t wc = L'あ' ;
  
  int x = 0 ;
  x = c16 ; // xの値は0x3042
  x = c32 ; // xの値は0x3042
  x = wc ; // xの値は実装依存


int型のサイズは、実装により異なるので、このコードは、実際のC++の実装では、動く保証はない。



基底型が指定されていないunscoped enum型は、int、unsigned int、long int、unsigned long int、long long int、unsigned long long intのうち、enum型のすべての値を表現できる最初の型に変換できる。もし、どの標準整数型でもすべての値を表現できない場合、すべての値を表現できる実装依存の拡張整数型のうち、もっとも変換順位の低い型が選ばれる。もし、順位の同じ整数型が二つある場合。つまり、signedとunsignedとが違う場合、signedな整数型の方が選ばれる。



基底型が指定されてるunscoped enum型は、指定された基底型に変換できる。その場合で、さらに整数のプロモーションが適用できる場合も、プロモーションとみなされる。例えば、



.. code-block:: c++
  
  enum E : short { value } ;
  
  short s = value ;// これは整数のプロモーション
  int i = value ; // これも整数のプロモーション


このように、enumの場合は、int型以外への変換でも、プロモーションになる。



int型への代入では、enum型が、基底型であるshortに変換された後、さらにintに変換されている。これは、どちらもプロモーションである。



<a href="#class.bit">ビットフィールド</a>は、すべての値を表現できる場合、intに変換できる。



.. code-block:: c++
  
  struct A
  {
      int x:8 ;
  } ;
  
  int main()
  {
      A a = {0} ;
      int x = a.x ;// 整数のプロモーション
  }


もし、ビットフィールドの値が、intより大きいが、unsigned int型で表現できる場合は、unsigned intに変換できる。値がunsigned intより大きい場合は、整数のプロモーションは行われない。整数の型変換が行われる。



bool型の値は、int型に変換できる。falseは0となり、trueは1となる。



.. code-block:: c++
  
  int a = true ; // aは1
  int b = false ; // bは0


以上が、整数のプロモーションである。これに当てはまらない整数型同士の型変換は、すべて、次に述べる<a href="#conv.integral">整数の型変換</a>である。


整数の型変換（Integral conversions）
--------------------------------------------------------------------------------



整数型は、他の整数型に型変換できる。ほんの一例を示すと、



.. code-block:: c++
  
  short s = 0 ;
  int i = s ;// shortからintへの変換
  s = i ; // intからshortへの変換
  
  unsigned int ui = i ; // intからunsigned intへの変換
  i = ui ; // unsigned intからintへの変換
  
  long l = s ; // shortからlongへの変換
  long long ll = l ; // longからlong longへの変換。


<a href="#conv.prom">整数のプロモーション</a>以外の整数の型変換は、すべて、整数の型変換になる。この違いは、オーバーロード解決などに影響するので、重要である。



整数の型変換は、危険である。変換先の型が、変換元の値を表現できない場合がある。



例えば、今、signed charは8ビットで、intは16ビットだと仮定する。



.. code-block:: c++
  
  #include <limits>
  
  int main()
  {
      int i = std::numeric_limits<signed char>::max() + 1 ;
      signed char c = i ;// どうなる？
  }


signed charは、intの取りうる値をすべて表現できるわけではない。この場合、どうなってしまうのか。



変換先の整数型がunsignedの場合、結果の値は、変換元の対応する下位桁の値である。



具体的な例を示して説明する。



.. code-block:: c++
  
  // unsigned charが8ビット、unsigned intが16ビットとする
  
  int main()
  {
      unsigned int ui = 1234 ;
      unsigned char uc = ui ; // 210
  }


この場合、unsigned int型は、16ビット、uiの値は、2進数で0000010011010010である。unsigned char型は8ビット。つまり、この場合の対応する下位桁の値は、2進数で11010010（uiの下位8ビット）である。よって、ucは、10進数で210となる。



unsignedの場合、変換先の型が、変換元の値を表現できないとしても、その値がどうなるかだけは、保証されている。もっとも、値を完全に保持できないので、危険なことには変わりないのだが。



変換先の整数型がsignedの場合は、非常に危険である。変換先の整数型が、変換元の値を表現できる場合、値は変わらない。表現できない場合、その値は実装依存である。



今仮に、int型は、signed char型の取りうる値をすべて表現できるが、signed char型は、int型の取りうる値をすべて表現することはできないとする。また、signed charは8ビット、intは16ビットとする。signed charの最小値は-127、最大値は127。intの最小値は-32767、最大値は32767とする。



.. code-block:: c++
  
  int main()
  {
      signed char c = 100 ;
      int i = c ; // iの値は100
  
      signed char value = 1000 ; // 値は実装依存
  
  }


iの値は、100である。なぜなら、今仮定した環境では、int型は100を表現できるからである。valueの値は、実装依存であり、分からない。なぜならば、signed char型は、1000を表現できないからだ。その場合、変換先のsignedな整数型の値は、実装依存である。


浮動小数点数のプロモーション（Floating point promotion）
--------------------------------------------------------------------------------



float型の値は、double型の値に変換できる。このとき、値は変わらない。つまり、floatからdoubleへの変換は、まったく同じ値が表現できることを意味している。



.. code-block:: c++
  
  float f = 3.14 ;
  double d = f ; // dの値は3.14


この変換を、浮動小数点数のプロモーションという。


浮動小数点数の型変換（Floating point conversions）
--------------------------------------------------------------------------------



浮動小数点数のプロモーション以外の、浮動小数点数同士の型変換を、浮動小数点数の型変換という。



.. code-block:: c++
  
  double d = 0.0 ;
  float f = 0.0 ;
  long double ld = 0.0 ;
  
  f = d ; // doubleからfloatへの型変換
  ld = f ; // floatからlong doubleへの型変換
  ld = d ; // doubleからlong doubleへの型変換


もし、変換先の型が、変換元の型の値を、すべて表現できるのならば、値は変わらない。値を正確に表現できない場合は、最も近い値が選ばれる。この近似値がどのように選ばれるかは、実装依存である。近似値すら表現できない場合の挙動は、未定義である。


浮動小数点数と整数の間の型変換（Floating-integral conversions）
--------------------------------------------------------------------------------



浮動小数点数型は、整数型に変換できる。このとき、小数部分は切り捨てられる。小数部分を切り捨てた後の値が、変換先の整数型で表現できない場合、挙動は未定義である。



.. code-block:: c++
  
  int x = 1.9 ;// xの値は、1
  int y = 1.9999 ; // yの値は、1
  int z = 0.9999 ; // zの値は、0


整数型、あるいはunscoped enum型は、浮動小数点数型に変換できる。結果は、可能であれば、まったく同じ値になる。近似値で表現できる場合、実装依存の方法によって、近似値が選ばれる。値を表現できない場合の挙動は、未定義である。



.. code-block:: c++
  
  float f = 1 ;// fの値は、1.0f


ポインターの型変換（Pointer conversions）
--------------------------------------------------------------------------------



nullポインター定数とは、整数型定数で、0であるものか、std::nullptr_t型である。



.. code-block:: c++
  
  0 ; // nullポインター定数
  1 ; // これはnullポインター定数ではない
  nullptr ; // nullポインター定数。型はstd::nullptr_t


0がnullポインター定数として扱われるのは、歴史的な理由である。




nullポインター定数は、どんなポインター型にでも変換できる。この値を、nullポインター値（null pointer value）という。nullポインター定数同士を比較すると、等しいと評価される。



.. code-block:: c++
  
  int * a = nullptr ;
  char * c = nullptr ;
  int ** pp = nullptr ;
  
  bool b = (nullptr == nullptr) ; // true


nullポインター定数を、CV修飾付きの型へのポインターに変換する場合、このポインターの型変換のみが行われる。CV修飾子の型変換ではない。



.. code-block:: c++
  
  // ポインターの型変換のみが行われる。
  // CV修飾子の型変換は行われない。
  int const * p = nullptr ;


整数型定数のnullポインター定数は、std::nullptr_t型に変換できる。結果の値は、nullポインターである。



.. code-block:: c++
  
  std::nullptr_t null = 0 ;


あるオブジェクトへのポインター型は、voidへのポインターに変換できる。



.. code-block:: c++
  
  int x = 0 ;
  int * int_pointer = &x ;
  void * void_pointer = int_pointer ;// int *からvoid *に変換できる


この時、CV修飾子が付いていた場合、消すことはできない。



.. code-block:: c++
  
  int x = 0 ;
  int const * int_pointer = &x ;
  
  void * error = int_pointer ; // エラー
  void const * ok = int_pointer ; // OK


void *に変換した場合、ポインターの値は、変換元のオブジェクトのストレージの、先頭を指し示す。値がnullポインターの場合は、変換先の型のnullポインターになる。



派生クラスのポインターから、基本クラスのポインターに変換することができる。



.. code-block:: c++
  
  struct Base { } ;
  struct Derived : Base { } ;
  
  D * p = nullptr ;
  Base * bp = p ; // OK。Derived *からBase *への変換


もし、基本クラスにアクセス出来ない場合や、曖昧な場合は、エラーとなる。



.. code-block:: c++
  
  // 基本クラスにアクセス出来ない場合
  struct Base { } ;
  struct Derived : private Base { } ;
  
  Derived * d = nullptr ;
  Base * b = d ;// エラー。Baseにはアクセス出来ないので、変換できない


.. code-block:: c++
  
  // 曖昧な場合
  struct Base { } ;
  struct Wrap1 : Base { } ;
  struct Wrap2 : Base { } ;
  
  // Derivedは、基本クラスとしてふたつのBaseを持っている。
  struct Derived : Wrap1, Wrap2 { } ;
  
  Derived * ptr = nullptr ;
  
  // エラー
  // Wrap1::Baseと、Wrap2::Baseのどちらなのかが曖昧
  Base * ambiguous_base = ptr ;
  
  // OK
  // Wrap1::Base
  Base * Wrap1_base = static_cast<Wrap1 *>(ptr) ;


派生クラスのポインターから基本クラスポインターへの変換の結果は、派生クラスの中の、基本クラス部分を指す。これは、変換の結果、ポインターの値が変わる可能性がある。実装に依存するので、あまり具体的な例を挙げたくはないが、例えば、以下のようなコードは、多くの実装で、ポインターの値が変わる。



.. code-block:: c++
  
  #include <cstdio>
  
  struct Base1 { int x ; } ;
  struct Base2 { int x ; } ;
  struct Derived : Base1, Base2 { } ;
  
  
  
  int main()
  {
      Derived d ;
  
      // dへのポインター
      Derived * d_ptr = &d ;
      std::printf("d_ptr : %p\n", d_ptr) ;
  
      // 基本クラスのポインターへ型変換
      Base1 * b1_ptr = d_ptr ;
      Base2 * b2_ptr = d_ptr ;
  
      // 多くの実装では、
      // b1_ptrとb2_ptrのどちらかが、d_ptrと同じ値ではない。
      std::printf("b1_ptr : %p\n", b1_ptr) ;
      std::printf("b2_ptr : %p\n", b2_ptr) ;
  
      // 派生クラスへキャスト（標準型変換の逆変換）
      Derived * d_ptr_from_b1 = static_cast<Derived *>(b1_ptr) ;
      Derived * d_ptr_from_b2 = static_cast<Derived *>(b2_ptr) ;
  
      // 多くの実装では、
      // d_ptrと同じ値になる。
      std::printf("d_ptr_from_b1 : %p\n", d_ptr_from_b1) ;
      std::printf("d_ptr_from_b2 : %p\n", d_ptr_from_b1) ;
  }


このように、基本クラスと派生クラスの間のポインターのキャストは、ポインターの値の変わる可能性がある。このような型変換には、単に値をそのまま使う、<a href="#expr.reinterpret.cast">reinterpret_cast</a>は使えない。



変換元のポインターの値がnullポインターの場合は、変換先の型のnullポインターになる。


メンバーへのポインターの型変換（Pointer to member conversions）
--------------------------------------------------------------------------------



nullポインター定数は、メンバーへのポインターにも変換できる。変換された結果の値を、nullメンバーポインター値（null member pointer value）という。



.. code-block:: c++
  
  struct C { int data ; } ;
  
  int C::* ptr = nullptr ;


nullメンバーポインター値は、他のメンバーへのポインターの値と比較できる。



.. code-block:: c++
  
  struct C { int data ; } ;
  
  int C::* ptr1 = nullptr ;
  int C::* ptr2 = &C::data ;
  
  bool b = ( ptr1 == ptr2 ) ; // false


boolの型変換（Boolean conversions）
--------------------------------------------------------------------------------



整数、浮動小数点数、unscoped enum、ポインター、メンバーへのポインターは、boolに変換できる。ゼロ値、nullポインター値、nullメンバーポインター値は、falseに変換される。それ以外の値はすべて、trueに変換される。



.. code-block:: c++
  
  bool b1 = 0 ; // false
  bool b2 = 1 ; // true
  bool b3 = -1 ; // true
  
  bool b4 = nullptr ; // false
  
  int x = 0 ; 
  bool b5 = &x ; // true


