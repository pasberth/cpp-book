テンプレート(Templates)
================================================================================

テンプレート仮引数/実引数(Template parameters/arguments)
--------------------------------------------------------------------------------



テンプレート仮引数(template parameters)は、テンプレート側で記述する引数である。テンプレート実引数は、テンプレートに与える引数である。本来、テンプレート仮引数とテンプレート実引数は明確に別の機能であるが、本書では分かりやすさを重視して、同時に説明する。



テンプレート仮引数と実引数には、型、非型、テンプレートがある。ここでは、テンプレート仮引数の宣言方法とテンプレート実引数の渡し方を説明する。



型テンプレート仮引数/実引数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



型を引数に取るテンプレート仮引数は、classまたはtypenameというキーワードに続いて、テンプレート仮引数名を記述する。classとtypenameには、意味上の違いはない。



.. code-block:: c++
  
  template < typename T >
  class X ;
  
  template < class T >
  class Y ;
  
  // 複数の引数を取る場合は、,で区切る
  template < typename T, typename U >
  classs X ;


テンプレート実引数は、テンプレート名に続いて、&lt; &gt;で実引数を囲んで渡す。



.. code-block:: c++
  
  template < typename T >
  void f() { }
  
  template < typename T >
  struct X { } ;
  
  int main( )
  {
      // テンプレート実引数 int
      f<int>() ;
      // テンプレート実引数 int
      X<int> x ;
  }


テンプレート仮引数は、テンプレートコードの中で、あたかも型や値であるかのように使うことができる。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      // T型のデータメンバーmemberの宣言
      T member ;
  } ;


Tの具体的な型は、テンプレート実引数が与えられたときに、すなわち、テンプレートが実体化したときに決定される。




非型テンプレート仮引数/実引数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



非型テンプレート仮引数(non-type template parameters)は、型以外、つまり値を引数に取る。非型テンプレート仮引数は、class/typenameと記述する代わりに、型を記述する。非型テンプレート仮引数に使える型は以下の通り。



* 
  
整数型とenum型



  .. code-block:: c++  
    
    // 整数型の一例
    template < int I, unsigned int UI, unsigned long long int ULLI >
    struct A { } ;
    
    // enum型の例
    enum struct E : int { value = 0 } ;
    
    template < E value >
    struct B { } ;
    
    
    int main( )
    {
        // 非型テンプレート実引数
        A< 0, 0u, 0ull > a ;
        B< E::value > b ;
    }
  


* 
  
オブジェクトへのポインターと、関数へのポインター



  .. code-block:: c++  
    
    // オブジェクトへのポインター
    template < int * P >
    struct A { } ;
    
    // 関数へのポインター
    using func_ptr_type = void (*)() ;
    
    template < func_ptr_type FUN >
    struct B { } ;
    
    void f() { }
    static int global = 0 ;
    
    int main( )
    {
        // 非型テンプレート実引数
        A< &global > a ;
        B< &f > b ;
    }
  


* 
  
オブジェクトへのlvalueリファレンスと関数へのlvalueリファレンス



  .. code-block:: c++  
    
    // オブジェクトへのlvalueリファレンス
    template < int & P >
    struct A { } ;
    
    // 関数型のtypedef名
    using func_type = void () ;
    // 関数へのlvalueリファレンス
    template < func_type & FUN >
    struct B { } ;
    
    void f() { }
    static int global = 0 ;
    
    int main( )
    {
        // 非型テンプレート実引数
        A< global > a ;
        B< f > b ;
    }
  


* 
  
メンバーへのポインター



  .. code-block:: c++  
    
    struct X
    {
        int member ;
    } ;
    
    // メンバーへのポインター
    template < int X::* P >
    struct Y { } ;
    
    int main( )
    {
        Y< &X::member > y ;
    }
  


* 
  
std::nullptr_t



  .. code-block:: c++  
    
    template < std::nullptr_t N >
    struct X { } ;
    
    X< nullptr > x ;
  




非型かつ非リファレンスのテンプレート仮引数はprvalueであり、いかなる方法を持っても代入などの値の変更をすることはできない。アドレスを取得することはできない。リファレンスに束縛される場合には、一時オブジェクトが使われる。



.. code-block:: c++
  
  template < int I >
  void f()
  {
  // 値の変更はできない
      I = 0 ; // エラー
      ++I ; // エラー
  
  // アドレスの取得はできない
      int * p = &I ; // エラー
  
  // リファレンスの束縛には一時オブジェクトがつかわれる
      int const & ref = I ;
  }


非型テンプレート仮引数は、浮動小数点数型、クラス型、void型として宣言することはできない。



.. code-block:: c++
  
  // エラー
  template < double d >
  struct S1 ;
  
  struct X { }
  
  // エラー
  template < X x >
  struct S2 ;
  
  // エラー
  template < void v >
  struct S3 ;


非型テンプレート仮引数の型が、「T型への配列」や、「T型を返す関数」である場合、それぞれ、「T型へのポインター」、「T型を返す関数へのポインター」と、型が変換される。



.. code-block:: c++
  
  // int * a
  template < int a[5] > 
  struct S1 ;
  
  // int (*func)()
  template < int func() >
  struct S2 ;


非型テンプレート実引数は、厳しい制約を受ける。



整数型とenum型の非型テンプレート仮引数に対するテンプレート実引数は、以下のとおりである。



* 
  テンプレート仮引数の型に変換できる定数式



  .. code-block:: c++  
    
    template < int I >
    struct S { } ;
    
    
    int main()
    {
        S< 0 > s1 ;
        S< 1 + 1 > s2 ;
    
        constexpr int x = 0 ;
        S< x > s3 ;
    }
  


* 
  
非型テンプレート仮引数の名前



  .. code-block:: c++  
    
    template < int I >
    struct A { } ;
    
    template < int I >
    struct B
    {
        A<I> a ;
    } ;
  


* 
  
定数式の、静的ストレージ上のオブジェクトへのアドレスと関数で、リンケージを持つもの。



  .. code-block:: c++  
    
    int x = 0 ; 
    
    template < int * ptr >
    struct A { } ;
    
    
    int f() { return 0 ; }
    
    template < int (*func)() >
    struct B { } ;
    
    int main()
    {
        A< &x > a ; // OK
        B< &f > b ; // OK
    
        static int no_linkage = 0 ; // リンケージを持たない
        A< no_linkage > a2 ; // エラー
    }
  

  
これは、実際にはもっと複雑な条件だが、本書では省略する。



* nullポインター、nullメンバーポインターの値であると評価される定数式
* メンバーへのポインター


文字列リテラルをテンプレート実引数として渡すことはできない。配列の要素へのアドレスを渡すこともできない。




テンプレートテンプレート仮引数/実引数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



テンプレート仮引数は、テンプレートを実引数に取ることができる。これをテンプレートテンプレート仮引数、テンプレートテンプレート実引数と呼ぶ。



.. code-block:: c++
  
  template < typename T >
  struct A { } ;
  
  template <
      template < typename T >
      // ここはclassキーワードを使わなければならない
      class U 
  >
  struct B
  {
      // Uはテンプレートとして使える
      U<int> u ;
  } ; 
  
  int main()
  {
      B< A > b ;
  
      B< int > e1 ; // エラー
      B< 0 > e2 ; // エラー
  }


テンプレートテンプレート仮引数は、テンプレートを受け取る。テンプレートを受け取るテンプレートなので、「テンプレートテンプレート仮引数」となる。この宣言は、テンプレート仮引数自体が、さらにtemplateキーワードを使う文法になる。テンプレート仮引数の名前には、文法上の制約により、classキーワードを使わなければならない。



.. code-block:: c++
  
  // OK
  template < template < typename > class T >
  struct X { } ;
  
  // エラー
  template < template < typename > typename T >
  struct Y { } ;


テンプレートテンプレート仮引数に対するテンプレートテンプレート実引数は、クラステンプレートか、エイリアステンプレートでなければならない。



.. code-block:: c++
  
  // クラステンプレート
  template < typename T >
  struct A { } ;
  
  // エイリアステンプレート
  template < typename T >
  using B = T ;
  
  template < template < typename T > class U  >
  struct C
  {
      U<int> u ;
  } ; 
  
  int main()
  {
      C< A > a ; // クラステンプレート
      C< B > b ; // エイリアステンプレート
  }




デフォルトテンプレート実引数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



テンプレート仮引数には、デフォルトテンプレート実引数を指定することができる。デフォルトテンプレート実引数は、=に続けて実引数を記述する。



.. code-block:: c++
  
  template < typename T = int, int I = 0 >
  struct X { } ;
  
  int main()
  {
      
      X<> a ; // X< int, 0 >
      X< double > b ; // X< double, 0 >
      X< short, 1 > c ; // X< short, 1 >
  }


デフォルトテンプレート実引数は、可変引数テンプレートを除く、すべての種類のテンプレート仮引数（型、非型、テンプレート）に指定できる。



.. code-block:: c++
  
  // 型テンプレート
  template < typename T = int >
  struct X { } ;
  
  // 非型テンプレート
  template < int I = 123 >
  struct Y { } ;
  
  // テンプレートテンプレート
  template < template < typename > class TEMP = X >
  struct Z { } ;
  
  // エラー、可変引数テンプレートには指定できない
  template < typename ... T >
  struct Error { } ;


デフォルトテンプレート実引数は、クラステンプレートのメンバーのクラス外部での定義に指定することはできない。これは説明が難しい。この場合のテンプレート仮引数には、クラスのテンプレートと、クラスのメンバーのテンプレートがあるが、このどちらにも、デフォルトテンプレート実引数を指定することはできない。



.. code-block:: c++
  
  // クラステンプレートの定義
  template < typename T >
  struct X
  {
   // メンバー関数テンプレートの宣言
      template < typename U >
      void f() ;
  } ;
  
  // クラス外部での定義
  template < typename T = int > // エラー（クラスXのテンプレート）
  template < typename U = int > // エラー（クラスXのメンバーfのテンプレート）
  void X<T>::f()
  { } 


この場合、デフォルトテンプレート実引数を指定したい場合は、それぞれ、クラステンプレートの定義や、メンバーの宣言に指定しなければならない。



デフォルトテンプレート実引数は、friendクラステンプレートのメンバー宣言に指定することはできない。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      // エラー
      template < typename U = int > 
      friend class X ;
  } ;


デフォルトテンプレート実引数が、friend関数テンプレート宣言に指定された場合、そのfriend関数テンプレート宣言は、定義でなければならない。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      // エラー、宣言
      template < typename U = int > 
      friend void f() ;
  
      // OK、定義
      template < typename U = int > 
      friend void g() { }
  } ;


これは、friend関数の宣言は、定義となることができるためである。詳しくは、<a href="#class.friend">friend</a>を参照。



デフォルトテンプレート実引数が指定されているテンプレート仮引数に続くテンプレート仮引数には、デフォルトテンプレート実引数が指定されていなければならない。



.. code-block:: c++
  
  // エラー、後続のテンプレート仮引数にテンプレート実引数が指定されていない
  template < typename T = int, typename U >
  struct X ;


あるいは、後続のテンプレート仮引数は、可変引数テンプレート仮引数でなければならない。



.. code-block:: c++
  
  // OK
  template < typename T = int , typename ... Types >
  struct X { } ;


同じ宣言のテンプレート仮引数には、二度以上デフォルトテンプレート実引数を指定してはならない。



.. code-block:: c++
  
  // OK
  template < typename T = int> struct A ;
  template < typename T > struct A { } ;
  
  // OK
  template < typename T > struct B ;
  template < typename T = int > struct B { } ;
  
  // エラー
  template < typename T = int > struct C ;
  template < typename T = int > struct C { } ;


デフォルトテンプレート実引数に与える式に含まれる&gt;には注意が必要である。ネストされていない&gt;は、テンプレート宣言の終了とみなされる。



.. code-block:: c++
  
  // 文法エラー
  template < int i = 1 > 2 >
  struct X { } ;
  
  // OK
  template < int i = ( 1 > 2 ) >
  sturct Y { } ;


テンプレートテンプレート仮引数内のテンプレート仮引数にも、デフォルトテンプレート実引数を指定することができる。



.. code-block:: c++
  
  template < template < typename TT = int > class T >
  struct X
  {
      T<> a ; // T< int > 
  } ;




可変テンプレート仮引数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



識別子の前に...を記述したテンプレート仮引数は、仮引数パックの宣言となる。これは、可変引数テンプレート(Variadic Templates)のための仮引数の宣言である。詳しくは、<a href="#temp.variadic">可変引数テンプレート</a>を参照。



.. code-block:: c++
  
  template < typename ... Types >
  struct X { } ;




テンプレート特殊化の名前(Names of template specializations )
--------------------------------------------------------------------------------



特殊化されたテンプレートは、テンプレートID(template-id)によって参照できる。これは普通の名前とは違い、特殊化したテンプレート実引数を指定する。テンプレートidとは、テンプレート名に続いて、&lt;を記述してテンプレート実引数を記述し、&gt;で閉じることによって記述できる。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  X テンプレート名
  X<int> テンプレートXをintに特殊化したテンプレートID


型の同一性(Type equivalence)
--------------------------------------------------------------------------------



二つのテンプレートidが同じクラスや関数であるためには、以下の条件を満たさなければならない。




* 
  
テンプレート名、演算子関数ID（オーバーロード演算子のテンプレートの場合）、リテラル演算子ID（オーバーロードリテラル演算子のテンプレートの場合）が同じ



* 
  
対応するテンプレート実引数の型が等しい。



* 
  
対応する非型テンプレート実引数の値が同じ。



  .. code-block:: c++  
    
    #include <type_traits>
    
    template < int I >
    class X { } ;
    
    
    int main()
    {
        std::cout << std::is_same< X<0>, X<0> >::value ; // true
        std::cout << std::is_same< X<0>, X<1> >::value ; // false
        std::cout << std::is_same< X<2>, X< 1 + 1 > >::value ; // true
    }
  


* 
  
対応する非型テンプレート実引数が、ポインター、メンバーへのポインター、リファレンスの場合、同じ外部オブジェクトを指し示していなければならない。ポインターとメンバーへのポインターの場合、nullポインターでもよい。



  .. code-block:: c++  
    
    #include <type_traits>
    
    template < int * P >
    class X { } ;
    
    int a ;
    int b ;
    
    int main()
    {
        std::cout << std::is_same< X<&a>, X<&a> >::value ; // true
        std::cout << std::is_same< X<&a>, X<&b> >::value ; // false
        std::cout << std::is_same< X<nullptr>, X<nullptr> >::value ; // true
    }
  


* 
  
対応するテンプレートテンプレート実引数が同じ。



  .. code-block:: c++  
    
    #include <type_traits>
    
    template < template < typename > class T >
    class X { } ;
    
    template < typename T >
    class Y { } ;
    template < typename T >
    class Z { } ;
    
    int main()
    {
        std::cout << std::is_same< X<Y>, X<Y> >::value ; // true
        std::cout << std::is_same< X<Y>, X<Z> >::value ; // false
    }
  




テンプレート宣言(Template declarations)
--------------------------------------------------------------------------------



クラステンプレート(Class templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



クラステンプレートはテンプレート仮引数に続けてクラス宣言を書くことで宣言できる。



.. code-block:: c++
  
  template < typename T, std::size_t SIZE >
  class Array 
  {
  private :
      T buf[SIZE] ;
  public :
  
      Array() : buf{}
      { }
  
      T & operator []( std::size_t i )
      { return buf[i] ; }
  
      T const & operator []( std::size_t i ) const
      { return buf[i] ; }
  
  } ;
  
  int main( )
  {
      Array< int, 10 > a ;
      a[3] = 100 ;
  }


テンプレート仮引数は、型や値やテンプレートとして使うことができ、テンプレートが実体化されたときにテンプレート実引数によって置き換えられる。



クラステンプレートのメンバー関数、メンバークラス、メンバーenum、staticデータメンバー、メンバーテンプレートを、メンバーが属するクラステンプレート定義の外部で定義する場合は、メンバー定義には、メンバーが属するひとつ外側のクラステンプレートのテンプレート仮引数を記述し、さらにメンバーが属するひとつ外側のクラステンプレートのテンプレート名に続けてテンプレート実引数リストを、同じ順番で記述しなければならない。



.. code-block:: c++
  
  template < typename T >
  class Outer
  {
      // クラス定義内部のでのメンバーの宣言
      void member_function() ;
      class member_class ; 
      enum struct member_enum : int ;
      static int static_data_member ;
  
      template < typename U >
      class member_template ;
  } ;
  
  // クラス定義外部でのメンバーの定義
  
  // メンバー関数
  template < typename T >
  void Outer<T>::member_function() { }
  
  // メンバークラス
  template < typename T >
  class Outer<T>::member_class { } ;
  
  // メンバーenum
  template < typename T >
  enum struct Outer<T>::member_enum : int
  { value = 1 } ;
  
  // staticデータメンバー
  template < typename T >
  int Outer<T>::static_data_member ;
  
  // メンバーテンプレート
  // クラス以外のテンプレートも同じ方法で記述する
  template < typename T > // Outerのテンプレート仮引数
  template < typename U > // member_templateのテンプレート仮引数
  class Outer<T>::member_template { } ;


これは、一見すると、恐ろしいほど難しそうに見えるが、クラスのメンバーをクラス定義の外部で宣言する文法に、テンプレート仮引数が加わっただけだ。ただし、メンバーテンプレートの定義方法だけは、少し分かりにくい。クラステンプレートのメンバーテンプレートには、メンバーテンプレートのテンプレート仮引数と、メンバーテンプレートが属するクラステンプレートのテンプレート仮引数の、両方が必要だからだ。



もちろん、メンバーはいくらでもネストできるので、宣言はもっと複雑になることもある。



.. code-block:: c++
  
  template < typename T >
  class Outer
  {
      template < typename U >
      class Inner
      {
          template < typename V >
          class Deep ;
      } ;
  } ;
  
  template < typename T > // Outerのテンプレート仮引数
  template < typename U > // Innerのテンプレート仮引数
  template < typename V > // Deepのテンプレート仮引数
  class Outer<T>::Inner<U>::Deep { } ;




メンバーテンプレート(Member Templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



テンプレートは、クラス定義の内部で宣言することができる。そのようなテンプレートを、メンバーテンプレート(Member Templates)と呼ぶ。



.. code-block:: c++
  
  class Outer
  {
      // メンバーテンプレート
      template < typename T >
      class Inner { } ;
  } ;


メンバーテンプレートは、クラス定義の内部でも外部でも定義できる。メンバーをクラス定義の外で定義する方法については、<a href="#temp.class">クラステンプレート(Class templates)</a>を参照。



メンバーテンプレートには、いくつかの制限や例外的なルールが存在する。



ローカルクラスはメンバーテンプレートを持つことができない。



.. code-block:: c++
  
  void f()
  {
      // エラー、
      template < typename T >
      class X { } ;
  }


デストラクターはメンバーテンプレートとして宣言できない。



.. code-block:: c++
  
  class X
  {
      // エラー
      template < typename T >
      ~X() { } 
  } ;


メンバー関数テンプレートはvirtual関数にはできない。



.. code-block:: c++
  
  class X
  {
      // エラー
      template < typename T >
      virtual void f() ;
  } ;


また、メンバー関数テンプレートの特殊化は基本クラスのvirtual関数をオーバーライドすることはない。



.. code-block:: c++
  
  struct Base
  {
      virtual void f( int ) ;
  } ;
  
  struct Derived : Base
  {
      template < typename T >
      void f( T ) ; // Base::fをオーバーライドしない
  } ;




可変引数テンプレート(Variadic Templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



可変引数テンプレート(Variadic templates)は、0個以上のテンプレート実引数や関数実引数を取るテンプレートのことである。



テンプレート仮引数の宣言で、識別子の前に...が記述されているとき、これをテンプレート仮引数パック(Template parameter pack)と呼ぶ。




.. code-block:: c++
  
  // 型テンプレート仮引数パック
  template < typename ... Type_pack >
  class X { } ;
  
  // 非型テンプレート仮引数パック
  template < int ... Int_pack >
  class Y { } ;
  
  // テンプレートテンプレート仮引数パック
  template < template < typename > class ... Template_pack >
  class Z { } ;
  
  // テンプレート実引数として与えるためのテンプレート
  template < typename T >
  class Arg { } ;
  
  int main( )
  {
      X< > x1 ;
      X< int > x2 ; 
      X< int, int, double, float > x3 ;
  
      Y< > y1 ;
      Y< 0 > y2 ;
      Y< 1, 2, 3, 4, 5 > y3 ;
  
      Z< > z1 ;
      Z< Arg > z2 ;
      Z< Arg, Arg, Arg > z3 ;
  }


上記の例のように、テンプレート仮引数パックは、0個以上の任意の数のテンプレート実引数を取る。



非型テンプレート仮引数として、オブジェクトや関数へのポインターやリファレンスなども可変引数テンプレートにできる。ただし、記述方法が少し分かりにくい。そのため、直接書くよりもtypedef名を使う方が読みやすくなる。



.. code-block:: c++
  
  // やや読みにくい宣言
  template < void ( * ... func_pack ) () >
  class X { } ;
  
  using type = void (*)() ;
  // 読みやすい宣言
  template < type ... func_pack >
  class Y { } ;


可変引数テンプレートをテンプレート実引数に取るテンプレートテンプレート仮引数は、以下のように書く。



.. code-block:: c++
  
  // 可変引数テンプレートを取る可変引数テンプレート
  template <
      template < typename Type > class Template
  >
  class X { } ;
  
  // テンプレート実引数に渡すテンプレート
  template < typename ... Type_pack >
  class Arg { } ;
  
  int main( )
  {
      X< Arg > x ;
  }


もちろん、このクラステンプレートXを、さらに可変引数テンプレートにすることもできる。



.. code-block:: c++
  
  // 可変引数テンプレートを取る可変引数テンプレート
  template <
      template < typename ... Type_pack > class ... Template_pack
  >
  class X { } ;
  
  // テンプレート実引数に渡すテンプレート
  template < typename ... Type_pack >
  class Arg { } ;
  
  int main( )
  {
      X< Arg, Arg, Arg > x ;
  }


関数仮引数パック(function parameter pack)は、テンプレート仮引数パックを使って、0個以上の関数の実引数を得る関数仮引数である。宣言方法は、関数の仮引数の識別子の前の...を記述する。



.. code-block:: c++
  
  // 任意の型の0個以上の実引数をとる関数
  template < typename ... template_parameter_pack >
  void f( template_parameter_pack ... function_parameter_pack ) { }
  
  int main( )
  {
      f( ) ;
      f( 1 ) ;
      f( 1, 2, 3, 4, 5 ) ;
  }


テンプレート仮引数パックと関数仮引数パックをあわせて、仮引数パック(Parameter pack)という。



仮引数パックは、そのままでは使えない。仮引数パックを使うには、展開しなければならない。これをパック展開(Pack expansion)という。パック展開は、パターンと...を組み合わせて記述する。テンプレートの実体化の際に、0個以上の実引数が、パターンに合わせて展開される。パターンの範囲は文脈により異なるが、見た目上は、仮引数パックを含む文字列を繰り返しているように見えるよう設計されている。



.. code-block:: c++
  
  template < typename ... pack >
  struct type_list_impl { } ;
  
  template < typename ... pack >
  struct type_list
  {
      using type = type_list_impl<
          pack // パターン
          ... 
      > ;
  } ;
  
  int main()
  {
      // type_list_impl<>
      type_list<>::type t1 ; 
      // type_list_impl<int, int>
      type_list<int, int>::type t2 ;
  }


この例では、type_listの仮引数パックであるpackをパック展開して、type_list_implのテンプレート実引数に渡している。"pack..."というのが、パック展開である。packがパターンだ。この場合は、そのまま展開している。



関数仮引数パックの場合も同様である。



.. code-block:: c++
  
  template < typename ... Types >
  void f_impl( Types ... pack ) { }
  
  template < typename ... Types >
  void f( Types ... pack )
  {
      f_impl( pack... ) ;
  }
  
  int main()
  {
      // f_impl( )を呼ぶ
      f( ) ;
      // f_impl( 1, 2, 3 )を呼ぶ
      f( 1, 2, 3 ) ;
  }


ここでも、"pack..."がパック展開で、packがパターンになっている。



パターンの記述は、パック展開の文脈に依存する。パック展開中の仮引数パックに対するパターンには、その文脈で許される記述をすることができ、そのパターンによって展開される。



.. code-block:: c++
  
  template < typename T >
  struct wrap { } ;
  
  
  template < typename ... pack >
  struct type_list_impl { } ;
  
  template < typename ... pack >
  struct type_list
  {
      using pointers = type_list_impl<
          pack *...
      > ;
  
      using references = type_list_impl<
          pack &...
      > ;
  
      using wraps = type_list_impl<
          wrap<pack>...
      > ;
  } ;
  
  int main()
  {
      // type_list_impl< char *, short *, int * >
      type_list< char, short, int >::pointers t1 ;
  
      // type_list_impl< char &, short &, int & >
      type_list< char, short, int >::references t2 ;
  
      // type_list_impl< wrap<char>, wrap<short>, wrap<int> >
      type_list< char, short, int>::wraps t3 ;
  }


packがテンプレート仮引数パックであるならば、pack * ...はそれぞれの実引数に*を加えたパターンとして展開される。wrap&lt;pack&gt;は、それぞれの実引数をクラステンプレートwrapの実引数に渡すパターンとして展開される。



関数仮引数パックの場合も同様。



.. code-block:: c++
  
  template < typename ... param_pack >
  void f( param_pack ... ) { } // 仮引数名の省略
  
  template < typename T >
  T identity( T value )
  {
      return value ;
  }
  
  template < typename ... param_pack >
  void g( param_pack ... pack )
  {
      f( pack ... ) ; // そのまま関数fに渡す
      f( (pack + 1)... ) ; // +1して関数fに渡す
      f( identity(pack)... ) ; // identity()の評価の結果を関数fに渡す
  
  }
  
  int main( )
  {
      g( ) ;
      g( 1 ) ;
      g( 1, 2, 3, 4, 5 ) ;
  
  }


パック展開できる文脈は限られているが、一般に、型や式をコンマで区切って記述する文脈に書くことができる。



まず、特別なパック展開が三種類ある。ただし、規格上は区別されてない。この特別なパック展開は、パック展開でありながら、仮引数パックでもあるという特徴を持つ。



* 
  
関数仮引数パックの宣言



  
関数仮引数パックの宣言は、...以外がそのままパック展開のパターンにもなる。そのため、これは仮引数パックかつパック展開となる。



  .. code-block:: c++  
    
    template < typename ... param_pack >
    void f( param_pack const & ... pack ) ;
  

  
この例では、"param const &amp;"がパターンとなる。



  
関数仮引数パックは、宣言自体がパターンとなっているので、実引数の型がパターンに一致しない場合、実引数推定が失敗する。これを利用して、型を部分的に限定することができる。



  .. code-block:: c++  
    
    // ポインター型しか実引数に指定できない関数
    template < typename ... Types >
    void f( Types * ... pack  )
    {　}
    
    int main( )
    {
        int * p = nullptr ;
        f( p ) ; // OK
        f( 123 ) ; // エラー
    }
  

  
同様に、メンバーへのポインターや、関数へのポインターに限定することもできる。



  .. code-block:: c++  
    
    // 実引数を取らず、任意の型を戻り値に返す関数へのポインターを実引数に取る関数
    template < typename ... ReturnType >
    void f( ReturnType (* ... pack) ( ) )
    { }
    
    void g( ) { }
    int h( ) { }
    double i( ) { }
    
    int main( )
    {
        f( &g, &h, &i ) ; 
    }
  

  
パターンは...を除いた部分なので、この場合のパターンは、"ReturnType (*)()"となる。つまり関数へのポインター型になっている。



  
もっと複雑な条件で型を限定したい場合は、テンプレートメタプログラミングの技法を使うことができる。その詳細は本書の範疇を超えるので、ここには書かない。




* 
  
テンプレート仮引数パックがパック展開となる場合



  
これには二種類ある。ひとつは、非型テンプレート仮引数パックの仮引数宣言に、先に宣言されたテンプレート仮引数が使われる場合。パターンは、...を除いた部分となる。



  .. code-block:: c++  
    
    template < typename T, /* パターンここから */ T * /* パターンここまで */... Types >
    struct X { } ;
    
    int main( )
    {
        X< int, nullptr > x ;
    }
  

  
この例では、"T *"がパターンとなっている。関数仮引数パックと同じように、実引数の型を制限できる。



  
もうひとつは、テンプレートテンプレート仮引数パックの中で、先に宣言されたテンプレート仮引数パックが使われる場合。パターンは...を除いた部分となる




  .. code-block:: c++  
    
    template< typename ... Types >
    struct Outer
    {
        template< template< Types > class ... pack >
        struct Inner ;
    } ;
  

  
これは少し分かりにくい。仮引数パックTypesのパック展開が、クラステンプレートInnerのテンプレート仮引数で行われている。パターンは、"template&lt; Types &gt; class"だ。



  
今、Outer&lt; char, short, int &gt;のようにテンプレート実引数が渡されたとすると、Innerのパック展開の結果を擬似的に記述すると、以下のようになる。。



  .. code-block:: c++  
    
    template < char, short, int >
    struct Outer
    {
        template <
            template < char > class pack_1,
            template < short > class pack_2,
            template < int > class pack_3
        >
        struct Inner ;
    } ;
  

  
つまり、テンプレートInnerのテンプレート仮引数は、テンプレートテンプレート仮引数がパターンで、仮引数パックであるTypesに対してパターンを適用してパック展開されることになる。



  
これはあくまで解説のための擬似的なコードである。可変引数テンプレートは、パックとパック展開という形で使うので、手で書いたようなテンプレートに展開されるわけではない。






その他のパック展開だけの文脈は以下の通り。



* 
  
初期化リストの中





  
関数呼び出し式の中の式リストも、初期化リストである。パターンは初期化子の式となる。



  .. code-block:: c++  
    
    struct X
    {
        template < typename ... pack >
        X( pack ... ) { }
    } ;
    
    template < typename ... Types >
    void f( Types ... pack ) { }
    
    template < typename ... Types >
    void g( Types ... pack )
    {
        X x( pack ... ) ; 
        f( pack... ) ;
        
        f( (pack + 1)... ) ;// パターンはpack+1
    }
  


* 
  
基本クラス指定リストの中



  
これにより、仮引数パックに対するすべての実引数の型を基本クラスに指定することができる。パターンは基本クラス指定子。



  .. code-block:: c++  
    
    template < typename ... pack >
    struct X : pack ...
    { } ;
    
    struct A { } ;
    struct B { } ;
    
    
    int main( )
    {
        X< > x1 ; // 基本クラスなし
        X< A > x2 ; // 基本クラスA
        X< B > x3 ; // 基本クラスB
        X< A, B > x4 ; // 基本クラスAとB
    
        X< int > x5 ; // エラー、intは基本クラスにできない
    }
  

  
複雑なパターンの例。



  .. code-block:: c++  
    
    template < typename T >
    struct wrap { } ;
    
    
    template < typename ... pack >
    struct X : wrap< pack > ...
    { } ;
    
    int main( )
    {
        // Xの基本クラスはwrap<int>とwrap<double>
        X< int, double > x ;
    }
  

  
この例では、テンプレート実引数はwrap&lt;T&gt;に包まれて基本クラスに指定される。そのため、直接intから派生するのではなく、テンプレートwrapの特殊化から派生することになる。




* 
  
メンバー初期化リスト



  
これは、初期化リストとほぼおなじだ。パターンはメンバー初期化子の式になる。



  .. code-block:: c++  
    
    struct X
    {
        template < typename ... pack >
        X( pack ... ) { }
    } ;
    
    struct Y
    {
        X x ;
        template < typename ... pack >
        Y( pack ... args )
            : x( args... )
        { }
    } ;
    
    int main( )
    {
        Y y( 1, 2, 3 ) ;   
    }
  


* 
  
テンプレート実引数リスト



  
パターンはテンプレート実引数。



  .. code-block:: c++  
    
    template < typename ... pack >
    struct X { } ;
    
    template < typename T >
    struct wrap { } ;
    
    template < typename ... pack >
    struct Y
    {
        // パターンはpack
        X< pack ... > x1 ;
        // パターンはwrap<pack>
        X< wrap<pack> ... > x2 ;
    } ;
  


* 
  
アトリビュートリスト



  
パターンはアトリビュート



  .. code-block:: c++  
    
    template < typename ... pack >
    struct X
    {
        [[ pack ... ]] ;
    
    } ;
  


* 
  
アライメント指定子



  
パターンは...を除いたアライメント指定子



  .. code-block:: c++  
    
    template < typename ... pack >
    struct X
    {
        alignas( pack ... ) int data_member ;
    } ;
  

  
たとえば、X&lt;int, short, double&gt;と実引数を与えると、この特殊化されたクラスXのデータメンバーdata_memberのアライメント指定は、alignas( int, short, double )と記述したものと等しくなる。




* 
  
キャプチャーリスト



  
パターンはキャプチャー



  .. code-block:: c++  
    
    template < typename ... Types >
    void f_impl( Types ... ) { }
    
    template < typename ... Types >
    void f( Types ... pack )
    {
        // キャプチャーのパターンは&pack
        [ &pack ... ]{ f_impl( pack... ) ; }() ;
    }
  

  
この例では、関数仮引数パックをパック展開して、ラムダ式でリファレンスキャプチャーしている。



* 
  
sizeof...式



  
sizeof...式も、パック展開の一種である。ただし、パターンは識別子なので、特に特別なことはできない。ただ、仮引数パックの数を返すだけだ。



  .. code-block:: c++  
    
    template < typename ... Types >
    int f( Types ... args )
    {
        sizeof...(Types) ; // 評価はテンプレート仮引数パックの数
        sizeof...(args) ; // 評価は関数仮引数パックの数
    
        return sizeof...(Types) ;
    }
    
    
    int main( )
    {
        f() ; // 評価は0
        f( 1, 2, 3 ) ; // 評価は3
    }
  




可変引数テンプレートの使い方
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



本書はコア言語の文法と機能を解説するものであって、使い方を紹介するものではない。ただし、可変引数テンプレートでは、最低限の使い方を解説する。



仮引数テンプレートは、仮引数パックによって、0個以上の実引数を取ることができる。ただし、仮引数パックはそのままでは使えない。仮引数パックは、仮引数ではないからだ。仮引数パックを使うには、パック展開しなければならない。では、一体どうやって、任意個の実引数に対応した汎用的なコードを書くのか。それには、二つ方法がある。固定長の仮引数を取るものに渡すか再帰だ。



固定長の仮引数を取るものに渡すというのは、単にパック展開して渡せばよい。



.. code-block:: c++
  
  #include <iostream>
  
  // 実引数ゼロ個の時は何もしない
  void print_impl( ) { }
  
  template < typename T1 >
  void print_impl( T1 a1 )
  {
      std::cout << a1 << std::endl ;
  }
  
  template < typename T1, typename T2 >
  void print_impl( T1 a1, T2 a2 )
  {
      std::cout << a1 << std::endl ;
      std::cout << a2 << std::endl ;
  }
  
  template < typename ... Types >
  void print( Types ... pack )
  {
      print_impl( pack ... ) ;
  }
  
  int main( )
  {
      print( ) ; // エラー
      print( 1 ) ; // OK
      print( 1, 2 ) ; // OK
      print( 1, 2, 3 ) ; // エラー
  }


問題は、コード例をみても分かるように、このコードは汎用的ではないという事だ。固定長の仮引数を持つ関数に渡しているために、固定長しか扱えない。これではせっかくの可変引数の意味がない。



固定長の仮引数を取るものに渡すというのは、特定の条件で、特別な処理をしたい場合に使えるが、汎用的に使うことはできない。



任意の個数の実引数に対応した汎用的なコードを書くためには、再帰を使う。



.. code-block:: c++
  
  // 再帰の終了条件
  void print(  ) { }
  
  template < typename T, typename ... Types >
  void print( T head, Types ... tail )
  {
      std::cout << head << std::endl ;
      print( tail ... ) ; // 再帰的実体化
  }
  
  int main( )
  {
      print( ) ; // エラー
      print( 1 ) ; // OK
      print( 1, 2 ) ; // OK
      print( 1, 2, 3 ) ; // OK
  }


再帰と言っても、同じ関数を再帰的に呼び出すわけではない。仮引数パックで受ける実引数の数をひとつづつ減らしていき、新たなテンプレートを実体化させて呼び出している。たとえば、print(1, 2, 3, 4, 5)を呼び出した場合、以下のように実体化されて呼び出される。



.. code-block:: c++
  
  print<int, int, int, int, int>( 1, 2, 3, 4, 5 )
  print<int, int, int, int>( 2, 3, 4, 5 )
  print<int, int, int>( 3, 4, 5 )
  print<int, int>( 4, 5 )
  print<int>( 5 ) 
  print() 


トリックは、実引数をすべて仮引数パックで受けるのではなく、一つを除いた残りを受ける形にすることだ。これにより、実引数をひとつづつ減らしながら再帰的にテンプレートを実体化して呼び出すことができる。ただし、仮引数パックは0個の実引数を受けることができるので、そのままではコンパイル時に無限ループしてしまう。コンパイル時無限ループを防ぎ、コンパイル時再帰を正しく終了させるために、仮引数を取らない非テンプレートな関数を用意している。オーバーロード解決により、非テンプレートな関数は、関数テンプレートの実体化より優先される。



また、仮引数パックを使わない関数テンプレートの実体化は、仮引数パックを使う関数テンプレートの実体化より、オーバーロード解決で優先される。たとえば、二つ以上の任意個の実引数を取り、最小の値を返す関数テンプレートminは、以下のように実装できる。



.. code-block:: c++
  
  // 終了条件
  template < typename T >
  T min ( T a1, T a2 )
  {
      return a1 < a2 ? a1 : a2 ;
  }
  
  template < typename T, typename ... Types >
  T min( T head, Types ... tail )
  {
      return min( head, min( tail ... ) ) ; 
  }


クラステンプレートのテンプレート仮引数パックの場合も、同様に、固定長へのパック展開か、再帰的な汎用コードが使える。



固定長へのパック展開の例は、以下の通り。



.. code-block:: c++
  
  template < typename T1, typename T2, typename T3 >
  struct type_list_impl
  { } ;
  
  
  template < typename ... pack >
  struct type_list
      : type_list_impl< pack ... >
  { } ;


明らかに、このコードは汎用的ではない。それに、クラステンプレートには、部分的特殊化があるので、このようなことはしなくても固定長への特殊化はできる。



.. code-block:: c++
  
  // Primary Class Template
  template < typename ... pack >
  struct type_list ; 
  
  template < typename T1 >
  struct type_list< T1 >
  { } ;
  
  template < typename T1, typename T2 >
  struct type_list< T1, T2 >
  { } ;
  
  template < typename T1, typename T2, typename T3 >
  struct type_list< T1, T2, T3 >
  { } ;


ただし、固定長の別の関数にパック展開する関数仮引数パックと同じように、固定長の部分的特殊化は、汎用的ではない。特定の条件に対する特殊な別の実装のためには適切であっても、汎用的なコードは書けない。



テンプレート仮引数パックを使うクラステンプレートを汎用的に書くには、再帰を使えばよい。再帰の方法として、再帰的に基本クラスから派生する方法と、再帰的にデータメンバーとして持つ方法がある。



.. code-block:: c++
  
  // 再帰的に基本クラスから派生する方法
  // primary class template
  template < typename ... >
  struct base_class_trick ;
  
  // 部分的特殊化
  template < typename Head, typename ... Tail >
  struct base_class_trick< Head, Tail ... >
      : base_class_trick< Tail ... >
  { } ;
  
  // 終了条件
  template <  >
  struct base_class_trick< >
  { } ;
  
  // 再帰的にデータメンバーとして持つ方法
  // primary template
  template < typename ... >
  struct data_member_trick ;
  
  // 部分的特殊化
  template < typename Head, typename ... Tail >
  struct data_member_trick< Head, Tail ... >
  {
      data_member_trick< Tail ... > tail ;
  } ;
  
  // 終了条件
  template < >
  struct data_member_trick< >
  { } ;


自分自身から派生したり、自分自身をデータメンバーに持っているわけではない。再帰のたびに、別の実体化を発動させるので、派生したりデータメンバーに持っているのは、別のクラスである。再帰の終了には、部分的特殊化か、明示的特殊化を使う。



これを応用して、任意のテンプレート実引数の型と数をコンストラクターで受け取り、クラスのデータメンバーとして格納するクラスが書ける。



.. code-block:: c++
  
  template < typename ... >
  struct tuple ;
  
  template < typename Head, typename ... Tail >
  struct tuple< Head, Tail ... >
      : tuple< Tail ... >
  {
          Head data ;
          tuple( Head const & head, Tail const & ... tail )
              : tuple< Tail ... >( tail ... ),
                data( head ) 
          { }
  } ;
  
  // 終了条件
  template < >
  struct tuple< >
  { } ;
  
  int main()
  {
      tuple< int, short, double, float > t( 12, 34, 5.6, 7.8f ) ;
  }


クラステンプレートtupleは、別の実体化から再帰的に派生する。実体化されたtupleは、それぞれ先頭のテンプレート実引数の型をデータメンバーとして持つ。コンストラクターは先頭の型の値と、仮引数パックからなる実引数を取り、先頭の値をデータメンバーに格納して、残りを基本クラスに投げる。これが再帰的に行われるため、すべての実引数を格納することができる。



ただし、tupleから値を取り出すのは、少し面倒だ。なぜならば、対応するクラスの型にキャストしなければならないからだ。



.. code-block:: c++
  
  int main( )
  {
      tuple< int, short, double, float > t( 12, 34, 5.6, 7.8f ) ;
      double d = static_cast< tuple< double, float> & >(t).data ;
  }


これも可変引数テンプレートを使って解決できる。何番目の値が欲しいか実引数として与えれば、その値を返してくれる関数テンプレートを書けばいい。インデックスは0から始まるとする。この関数テンプレートは、以下のような形になる。



.. code-block:: c++
  
  template < std::size_t I,  typename ... Types >
  戻り値の型 get( tuple< Types ... > & t )
  {
      return static_cast< 対応する値が格納されているクラス型 >(t).data ;
  }
  
  int main( )
  {
      tuple< int, short, double, float > t( 12, 34, 5.6, 7.8f ) ;
      auto value = get<2>( t ) ; // 5.6
  }


さて、戻り値の型はどうやって指定すればいいのか。それには、インデックスを指定すれば、その型を返してくれるメタ関数を書けばよい。




.. code-block:: c++
  
  template < std::size_t I, typename T  >
  struct tuple_element ;
  
  template < std::size_t I, typename Head, typename ... Types >
  struct tuple_element< I, tuple< Head, Types ... > >
      : tuple_element< I - 1, tuple < Types ... > >
  {
      static_assert( I < 1 + sizeof...( Types ), "index exceeds the tuple length." ) ;
  } ;
  
  template < typename Head, typename ... Types >
  struct tuple_element < 0, tuple< Head, Types ... > >
  {
      using type = Head ;
  } ;
  
  int main( )
  {
      using type = tuple< int, short, double, float > ;
      tuple_element< 2, type >::type d ; // double
  }


tuple_elementは、0から始まるインデックスを数値として指定すると、対応する型を、ネストされた型名typeとして返すメタ関数だ。



次に、キャストすべき型を返してくれるメタ関数をつくる。



.. code-block:: c++
  
  template < std::size_t, typename ... >
  struct tuple_get_type ;
  
  template < std::size_t I, typename Head, typename ... Tail >
  struct tuple_get_type< I, Head, Tail ... >
      : tuple_get_type< I-1, Tail ... >
  { } ;
  
  template < typename Head, typename ... Tail >
  struct tuple_get_type< 0, Head, Tail ... >
  {
      using type = tuple< Head, Tail ... > ;
  } ;
  
  
  int main()
  {
      // typeはtuple< double, float > 
      using type = tuple_get_type< 2, int, short, double, float >::type ; 
  }


この二つのメタ関数を合わせると、関数テンプレートgetは、以下のように書ける。



.. code-block:: c++
  
  template < std::size_t I,  typename ... Types >
  typename tuple_element< I, tuple< Types ... > >::type &
  get( tuple< Types ... > & t )
  {
      return static_cast< typename tuple_get_type<I, Types ... >::type & >(t).data ;
  }


まだまだ、面白い技法はたくさんあるのだが、本書はテンプレートメタプログラミングの解説書ではないので、ここで筆を止める。さらに深く調べたい者は、標準ライブラリのtupleやfunctionやbindから始めるといいだろう。もし十分な需要があれば、C++11によるテンプレートメタプログラミングの本も執筆するかもしれない。







friend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



friend宣言はテンプレートとして宣言できる。また、friend宣言はテンプレートの特殊化を指定できる。



非テンプレートなfriend宣言で、クラステンプレートや指定するには、特殊化を指し示していなければならない。関数テンプレートは、特殊化か、あるいは実引数推定されるものを指し示さなければならない。



.. code-block:: c++
  
  template < typename T >
  class X ;
  
  template < typename T >
  void f( T ) ;
  
  
  template < typename T >
  class Y
  {
      friend class X ; // エラー    
  
      friend class X<int> ; // OK
      friend void f( int ) ; // OK
  
      friend class X<T> ; // OK
      friend void f( T ) ; // OK 
      friend void f<double>(double) ; // OK
  
  } ;


friendで指定されたテンプレートの特殊化のみのがクラス、あるいはクラステンプレートのfriendとなる。その他の特殊化はfriendとはならない。



.. code-block:: c++
  
  template < typename T >
  void f( ) ;
  
  
  template < typename T >
  class X
  {
  private :
      int data ;
  
      friend void f<int>( ) ;
  } ;
  
  template < typename T >
  void f()
  {
      Y y ;
      y.data = 0 ;
  }
  
  int main( )
  {
      f<int>() ; // OK、f<int>はXのfriend
      f<double>() ; // エラー、f<double>はXのfriendではない
  }


friendテンプレートは、クラステンプレートと関数テンプレートの全ての実体化に対して働く。



.. code-block:: c++
  
  template < typename T >
  void f() ;
  
  template < typename T >
  struct Y { } ;
  
  class X
  {
  private :
      int data ;
  
      // 関数テンプレートfに対するfriendテンプレート
      template < typename T >
      friend void f() ;
      // クラステンプレートYに対するfriendテンプレート
      template < typename T >
      friend class Y ;
  
  } ;
  
  template < typename T >
  void f()
  {
      X x ;
      x.data = 0 ;
  }
  
  
  int main( )
  {
      f<int>() ; // OK
      f<double>() ; // OK
  }


クラステンプレートのすべての特殊化のメンバー関数をfriendにする場合は、friendテンプレートを使う。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      static void f() ;
  } ;
  
  class Y
  {
  private :
      int data ;
      // クラステンプレートXのすべての特殊化のメンバー関数fに対するfriendテンプレート
      template < typename T >
      friend void X<T>::f() ;
  } ;
  
  template < typename T >
  void X<T>::f()
  {
      Y y ;
      y.data = 0 ;
  }
  
  
  int main( )
  {
      X<int>::f() ; // OK
      X<double>::f() ; // OK
  }


friendテンプレートは、ローカルクラスでは宣言できない。



friendテンプレートは、部分的特殊化できない。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  struct Y
  {
      // エラー、部分的特殊化はできない
      template < typename T >
      friend struct X< T * > ;
  } ;




クラステンプレートの部分的特殊化(Class template partial specializations)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



クラステンプレートの部分的特殊化(Class template partial specializations)は、特殊化(specialization)という名前がついているが、テンプレートの実体化の結果生成される特殊化や、明示的特殊化とは異なる。これは部分的な特殊化であって、テンプレートである。



テンプレート宣言の際のテンプレート名が、識別子だけの基本となるクラステンプレートを、プライマリークラステンプレート(Primary class template)と呼ぶ。俗に、プライマリーテンプレートとも呼ばれる。



.. code-block:: c++
  
  // プライマリークラステンプレート
  template < typename T >
  class Identifier ; 


クラステンプレートの部分的特殊化は、この基準となるプライマリークラステンプレートの一部を特殊化するものである。その宣言方法は、先に宣言したテンプレートと同名で、テンプレート実引数を加えた形のテンプレートIDで宣言する。



.. code-block:: c++
  
  // プライマリークラステンプレートX
  template < typename T >
  struct X { } ;
  
  // Xの部分的特殊化
  template < typename T >
  struct X< T * >
  { } ;


プライマリークラステンプレートは、部分的特殊化よりも先に宣言されていなければならない。



部分的特殊化は、直接参照することはできない。部分的特殊化のあるテンプレートを使う際に、最もテンプレート実引数に対して特殊化されたテンプレートが選ばれて実体化される。



.. code-block:: c++
  
  // #1
  template < typename T >
  struct X { } ;
  // #2
  template < typename T >
  struct X< T * > { } ;
  // #3
  template < typename T >
  struct X< T & > { } ;
  
  int main( )
  {
      X< int > x1 ; // #1
      X< int * > x2 ; // #2
      X< int & > x3 ; // #3
  }


この例では、テンプレート実引数int *は、T *が最も特殊化されているので、#2が選ばれる。



部分的特殊化は、名前通り部分的に特殊化していればいい。一部に具体的な型や値やテンプレートを与えることもできる。



.. code-block:: c++
  
  // #1
  template < typename T1, typename T2 >
  struct X { } ;
  
  // #2
  template < typename T >
  struct X< T, T > { } ;
  
  // #3
  template < typename T >
  struct X< T, double > { } ;
  
  int main( )
  {    
      X< int, int > x1 ; // #2
      X< int, double > x2 ; // #3
  
      // エラー、曖昧
      X< double, double > x3 ;
  }


プライマリークラステンプレートを使うつもりがないのであれば、プライマリークラステンプレートは宣言するだけで、定義しなくてもよい。以下の例は、テンプレート実引数としてポインター型だけを受け取るテンプレートである。



.. code-block:: c++
  
  // プライマリークラステンプレートの宣言
  // 定義はしない
  template < typename T >
  struct RequirePointerType ;
  
  // 部分的特殊化
  template < typename T >
  struct RequirePointerType< T * > { } ;
  
  
  int main( )
  {
      RequirePointerType< int * > x1 ; // OK
      RequirePointerType< int > x2 ; // エラー、定義がない
  }


このテンプレートに、ポインター以外の型をテンプレート実引数として渡しても、定義がないために、エラーとなる。



部分的特殊化のテンプレート仮引数の数は、プライマリークラステンプレートには左右されない。ただ、部分的特殊化として、テンプレートIDに指定する仮引数の数が一致していればよい。



.. code-block:: c++
  
  // #1
  template < typename T >
  struct X { } ;
  
  // #2
  template < typename T, template < typename > class Temp >
  struct X< Temp<T> >
  { } ;
  
  int main( )
  {
      X< X<int> > x ;
  }


この例では、X&lt;int&gt;には#1のテンプレートが使われ、X&lt; X&lt;int&gt; &gt;には、#2のテンプレートが使われる。



テンプレートIDに与えるテンプレート実引数の数が、プライマリークラステンプレートに一致していなければ、エラーとなる。



.. code-block:: c++
  
  // #1
  template < typename T1, typename T2 >
  struct X { } ;
  
  // エラー
  template < typename T >
  struct X< T > ;
  
  // エラー
  template < typename T1, typename T2, typename T3 >
  struct X< T1, T2, T3 > ; 


また、プライマリークラステンプレートのテンプレート仮引数の種類、すなわち、型テンプレート、非型テンプレート、テンプレートテンプレートに一致していなければならない。



.. code-block:: c++
  
  // 型、非型(int型)、テンプレート
  template < typename T, int I, template < typename > class Temp >
  struct X  ;
  
  // OK
  template < typename T, template < typename T > class Temp >
  struct X< T, 0, Temp<T> > { } ;
  
  // エラー、テンプレート仮引数の種類が一致していない。
  template < typename T >
  struct X< 0, T, T > { } ;


テンプレートテンプレート仮引数の場合は、テンプレートテンプレート仮引数のテンプレート仮引数の数や種類にも対応していなければならない。



.. code-block:: c++
  
  // プライマリークラステンプレート
  template < template < typename > class Temp >
  struct X { } ;
  
  // エラー、テンプレートテンプレート仮引数のテンプレート仮引数の数が一致していない
  template < template < typename, typename > class Temp >
  struct X< Temp > ;
  
  // エラー、テンプレートテンプレート仮引数のテンプレート仮引数の種類が一致していない
  template < template < int > class Temp >
  struct X< Temp > ;


可変引数テンプレートの場合は、0個以上の任意の数に特殊化できる。



.. code-block:: c++
  
  // プライマリークラステンプレート
  template < typename ... >
  struct X ;
  
  template < typename T >
  struct X< T > ;
  
  template < typename T1, typename T2 >
  struct X< T1, T2 > ;
  
  template < typename T1, typename ... Rest >
  struct X< T1, Rest ... > ;


部分的特殊化は、プライマリークラステンプレートが宣言された名前空間スコープやクラススコープの外側で宣言できる。



.. code-block:: c++
  
  namespace NS
  {
  
  template < typename T >
  struct Outer
  {
      template < typename U >
      struct Inner ;
  } ;
  
  }
  
  
  template < typename T >
  template < typename U >
  struct NS::Outer< T >::Inner< U * > { } ;


部分的特殊化の宣言中のテンプレートIDの実引数には、いくつかの制限が存在する。



非型実引数の式は、部分的特殊化のテンプレート仮引数の識別子のみである時以外は、テンプレート仮引数とか関わってはならない。



.. code-block:: c++
  
  template < int I, int J >
  struct X ;
  
  // OK、識別子のみ
  template < typename I >
  struct X< I, I > ;
  
  // エラー、部分的特殊化のテンプレート仮引数が関わる式
  template < int I >
  struct X< I+1, I+2 > ;


非型実引数の型は、部分的特殊化のテンプレート仮引数に依存してはならない。



.. code-block:: c++
  
  template < typename T, T I >
  struct X ;
  
  // エラー
  template < typename T >
  struct X< T, 0 > ;
  
  template < int I, int ( * Array_ptr)[I] >
  struct Y ;
  
  int array[5] ;
  
  // エラー
  template < int I >
  struct Y< I, &array > ;


部分的特殊化の実引数リストは、プライマリークラステンプレートに暗黙的に生成される実引数リストと同一であってはならない。



.. code-block:: c++
  
  template < typename T1, typename T2 >
  struct X ;
  
  template < typename T1, typename T2 >
  struct X< T1, T2 > ;


部分的特殊化のテンプレート仮引数には、デフォルトテンプレート実引数は使えない。




部分的特殊化のテンプレート実引数には展開されていない仮引数パックがあってはならない。テンプレート実引数がパック展開ならば、最後に記述されなければならない。



.. code-block:: c++
  
  template < typename ... >
  struct X ;
  
  // エラー、展開されていない仮引数パック
  template < typename T, typename ... Pack >
  struct X< T, Pack > ;
  
  // エラー、仮引数パックは最後に記述されなければならない
  template < typename T, typename ... Pack >
  struct X< Pack ..., T > ;
  
  template < typename ... >
  struct wrap { } ;
  
  // OK
  template < typename ... Pack, typename T >
  struct X< wrap<Pack...>, T > ;


クラステンプレートの部分的特殊化の一致度の比較(Matching of class template partial specializations)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



クラステンプレートの部分的特殊化は、直接参照することはできない。クラステンプレートを使った時、プライマリークラステンプレートや部分的特殊化が比較され、最もテンプレート実引数に対して特殊化されたテンプレートが選ばれる。



.. code-block:: c++
  
  template < typename T >
  struct X { } ; // #1
  
  template < typename T >
  struct X< T * > { } ; // #2
  
  template < typename T >
  struct X< T const * > { } ; // #3
  
  
  int main( )
  {
      X< int > x1 ; // #1
      X< int * > x2 ; // #2
      X< int const * > x3 ; // #3
  }


最適なテンプレートは、テンプレート実引数が、部分的特殊化のテンプレート実引数に、いかに一致しているかを比較することにより選択される。




この比較は以下のように行われる。



* 
  
一致する部分的特殊化が、ただひとつだけ発見された場合、その部分的特殊化が選ばれる。



  .. code-block:: c++  
    
    // プライマリークラステンプレート
    template < typename T1, typename T2 >
    struct X { } ;
    
    // 部分的特殊化
    template < typename T1, typename T2 >
    struct X< T2, T1 > { } ;
    
    int main( )
    {
        X< int, int > x ; // 部分的特殊化が実体化される
    }
  

  
これは極端な例だが、この例では、部分的特殊化はプライマリーテンプレートと同一ではない。X&lt; int, int &gt;には、プライマリークラステンプレートと部分的特殊化の両方が一致するが、ただひとつの部分的特殊化が一致するために、部分的特殊化が選ばれる。



  
一致する部分的特殊化が一つでもある場合、プライマリークラステンプレートが使われることはない。




* 
  
二つ以上の一致する部分的特殊化が発見された場合、<a href="#temp.class.order">半順序</a>の規則により、最も特殊化されている部分的特殊化が選ばれる。もし、他のすべての部分的特殊化よりもさらに特殊化されている部分的特殊化が見つからない場合、結果は曖昧となり、エラーとなる。



  .. code-block:: c++  
    
    template < typename T >
    struct X { } ; // #1
    
    template < typename T >
    struct X< T const > { } ; // #2
    
    template < typename T >
    struct X< T const volatile > { } ; // #3
    
    int main( )
    {
        X< int const > x1 ; // #2
        X< int const volatile > x2 ; // #3
    
        X< int > x3 ; // #1
    }
  

  
以下のような場合は、曖昧でエラーとなる。



  .. code-block:: c++  
    
    template < typename T1, typename T2 >
    struct X { } ;
    
    template < typename T >
    struct X< T, int > { } ;
    
    template < typename T >
    struct X< int, T > { } ;
    
    
    int main( )
    {
        X< int, int > x ; // エラー、曖昧
    }
  

  
この例では、プライマリークラステンプレートと、二つの部分的特殊化の、どのテンプレートを使っても実体化できる。ただし、二つ以上の一致する部分的特殊化があるために、プライマリークラステンプレートは使われない。二つの部分的特殊化は、どちらがより特殊化されているとも決定できないので、曖昧となる。




* 
  
一致する部分的特殊化が発見されなかった場合、プライマリークラステンプレートが使われる。







部分的特殊化が一致するかどうかは、テンプレート実引数から、部分的特殊化のテンプレート実引数を導けるかどうかで判断される。




.. code-block:: c++
  
  template < typename T1, typename T2 >
  struct X { } ;
  
  template < typename T >
  struct X< T, T > { } ; // #1
  
  template < typename T >
  struct X< T, int > { } ; // #2
  
  template < typename T1, typename T2 >
  struct X< T1 *, T2 > {} ; // #3
  
  
  int main( )
  {
      X< int, int > x1 ; // #1, #2に一致
      X< short, int > x2 ; // #2に一致
      X< int *, int * > x3 ; // #1, #3に一致
      X< int const *, int const * > x4 ; // #1, #3に一致
      X< int *, int > x5 ; // #3に一致
  
      X< int, short > x6 ; // 一致する部分的特殊化なし
  }




クラステンプレートの部分的特殊化の半順序(Partial ordering of class template specializations)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



二つのクラステンプレートの部分的特殊化の間で、どちらがより特殊化されているかということを、半順序(partial ordering)という。クラステンプレートの部分的特殊化の半順序は、比較のために部分的特殊化を関数テンプレートに書き換えた上で、関数テンプレートの半順序に従って決定される。



<p class="todo">
関数テンプレートの半順序へのリンク



部分的特殊化の比較のための関数テンプレートへの書き換えは、以下のように行われる。



書き換えた関数テンプレートは、元の部分的特殊化と同じテンプレート仮引数を持つ。この関数テンプレートはひとつの仮引数をとる。仮引数の型は、元の部分的特殊化のクラステンプレート名に、テンプレート実引数として、部分的特殊化と同じ記述をしたものである。




たとえば、以下のような部分的特殊化の場合は、



.. code-block:: c++
  
  template < typename T1, typename T2, typename T3 >
  struct X { } ;
  
  template < typename T >
  struct X< T, T, T > { } ;


比較用の関数テンプレートへの書き換えは、以下のようになる。



.. code-block:: c++
  
  template < typename T >
  void f( X< T, T, T > ) ;


以下の二つの部分的特殊化を比較する場合、



.. code-block:: c++
  
  template < typename T1, typename T2, typename T3 >
  struct X { } ;
  
  // #1
  template < typename T1, typename T2 >
  struct X< T1, T1, T2 > { } ;
  
  // #2
  template < typename T >
  struct X< T, T, T > { } ;


以下のように、関数テンプレートに書き換えられて、関数テンプレートの半順序により判断される。



.. code-block:: c++
  
  // #1
  template < typename T1, typename T2 >
  void f( X< T1, T1, T2 > ) ;
  
  // #2
  template < typename T >
  void f( X< T, T, T > ) ;


この例では、#2の方がより特殊化されている。





クラステンプレートの特殊化のメンバー
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



プライマリークラステンプレートと部分的特殊化の間は別物である。それぞれ異なるメンバーの宣言と定義を持つ。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void foo() ;
  } ;
  
  template < typename T >
  struct X< T * >
  {
      void bar() ;
  } ;
  
  int main()
  {
      X< int > x1 ;
      x1.foo() ; // OK
      x1.bar() ; // エラー
  
      X< int * > x2 ;
      x2.foo() ; // エラー
      x2.bar() ; // OK
  } 


部分的特殊化のメンバーをクラススコープの外で定義する場合、部分的特殊化と同じテンプレート仮引数とテンプレート実引数を使わなければならない。



.. code-block:: c++
  
  template < typename T >
  struct X ;
  
  template < typename T >
  struct X< T * >
  {
      // メンバーの宣言
      void bar() ;
  } ;
  
  // メンバーの定義
  template < typename T >
  void X< T * >::bar() { }


メンバーテンプレートも部分的特殊化できる。



.. code-block:: c++
  
  template < typename T >
  struct class_template
  {
      // プライマリーメンバークラステンプレート
      template < typename U >
      struct member_template { } ;
  
      // 部分的特殊化
      template < typename U >
      struct member_template< U * > { } ;
  } ;






関数テンプレート(Function templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数テンプレートは、特定の型にとらわれない関数のテンプレートを記述できる。



.. code-block:: c++
  
  template < typename T >
  void f( T param ) { }


関数テンプレートは、クラステンプレートと同じように、テンプレート実引数を指定して実体化させ、呼び出すことができる。



.. code-block:: c++
  
  template < typename T >
  void f( T param ) { }
  
  int main( )
  {
      f<int>( 0 ) ;
      f<double>( 0.0 ) ;
  }


関数テンプレートは、テンプレート実引数を指定せずに呼び出すことができる。この場合、関数の実引数から、テンプレート実引数が導かれる。これを、実引数推定(Argument Deduction)という。



.. code-block:: c++
  
  template < typename T >
  void f( T param ) { }
  
  int main( )
  {
      f( 0 ) ; // f<int>
      f( 0.0 ) ; // f<double>
  }


実引数推定できない場合、エラーとなる。



.. code-block:: c++
  
  template < typename T >
  void f( T * param ) { }
  
  int main( )
  {
      f( 0 ) ; // エラー、実引数推定できない
  }


より詳しくは、<a href="#temp.deduct">テンプレートの実引数推定</a>を参照。





関数テンプレートのオーバーロード(Function Template Overloading)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数テンプレートはオーバーロードできる。オーバーロードは、関数テンプレートと通常の関数の区別なく記述できる。



.. code-block:: c++
  
  template < typename T >
  void f( T ) ;
  
  template < typename T >
  void f( T * ) ;
  
  void f( int ) ;


異なる複数の関数テンプレートが同じテンプレート実引数に対して実体化できる場合、それぞれ異なる実態を持つので、ODR違反とはならない。



たとえば、ある一つのプログラムを構成する二つのソースファイルがあり、それぞれ以下のように記述されていたとする。



.. code-block:: c++
  
  // ソースファイル1
  template < typename T >
  void f( T ) { }
  
  void g( int * p )
  {
      f( p ) ;
  }


.. code-block:: c++
  
  // ソースファイル2
  template < typename T >
  void f( T * ) { }
  
  void h( int * p )
  {
      f( p ) ;
  }


この場合、それぞれのテンプレートから、それぞれ実体化が行われ、異なる特殊化が使われる。ODR違反とはならない。




関数テンプレートのオーバーロードは、実体化された特殊化が、全く同じシグネチャであっても構わない。



.. code-block:: c++
  
  template < typename T > void f( ) ;
  template < int I > void f( ) ;


テンプレート仮引数が、関数テンプレートの仮引数リストや戻り値の型における式の中で参照された場合、その式は関数テンプレートのシグネチャの一部になる。これにより、式の違いによる異なる関数テンプレートを記述できる。



.. code-block:: c++
  
  template < int I >
  struct X { } ;
  
  template < int I, int J >
  X< I + J > f( X<I>, X<J> ) ; // #1の宣言
  
  template < int K, int L >
  X< K + L > f( X<K>, X<L> ) ; // #1の再宣言
  
  template < int I, int J >
  X< I - J > f( X<I>, X<J> ) ; // #2、これは#1とは異なる宣言


最初の二つの関数テンプレートは、同一の関数テンプレートである。しかし、#2は式が違うため、異なる関数テンプレートである。



この時、シグネチャの式を評価した結果が同じものを、「機能的に同一」という。シグネチャの式が同じものを「同一」という。機能的に同一だが、同一ではない二つの宣言がある場合、エラーとなる。



.. code-block:: c++
  
  template < int I >
  struct X { } ;
  
  template < int I >
  void f( X< I + 2 > ) ;
  
  template < int I >
  void f( X< I + 1 + 1 > ) ; // エラー、機能的に同一だが、シグネチャの式が同一ではない


ただし、規格上、実装はこの誤りを検出して報告する必要はない。したがって、このエラーはコンパイルで見つけることは期待できない。よく注意しなければならない。





関数テンプレートの部分的特殊化(Partial ordering of function templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



関数テンプレートがオーバーロードされている場合、どの関数テンプレートの特殊化を使うべきなのか曖昧になる。



.. code-block:: c++
  
  template < typename T >
  void f( T ) { } // #1
  
  template < typename T >
  void f( T * ) { } // #2
   
  int main()
  {
      int * p = nullptr ;
      f( p ) ; // #2の特殊化が呼ばれる
  
      void ( *fp ) ( int * ) = &f ; // #2の特殊化のアドレスを得る
  }


以下の文脈の場合、半順序(partial ordering)によって、最も特殊化されているテンプレートを決定する。



* 関数テンプレートの特殊化を呼び出す際のオーバーロード解決
* 関数テンプレートの特殊化のアドレスを取得するとき
* プレイスメントoperator newに一致するプレイスメントoperator deleteを選択するとき
* 
  
friend関数宣言、明示的実体化、明示的特殊化が、ある関数テンプレートの特殊化を参照しているとき



  .. code-block:: c++  
    
    template < typename T >
    void f( T ) { } // #1
    
    template < typename T >
    void f( T * ) { } // #2
    
    class X
    {
        int data ; 
        template < typename T >
        friend void f( T ) ; // #1をfriendに指定
    } ;
    
    // #2の明示的実体化
    template void f( int * ) ;
    
    
    // #1の明示的特殊化
    template < >
    void f<double>( double ) { }
  




半順序は、二つのテンプレートを、後述する方法によって変換して関数型とし、テンプレート実引数推定をして、どちらがより特殊であるかを選ぶ。



<p class="todo">
完全に理解してから書く。





エイリアステンプレート(Alias templates)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



宣言部分がエイリアス宣言のテンプレート宣言を、エイリアステンプレートと呼ぶ。エイリアステンプレートは、複数の型名をテンプレート化することができる。いわば、typedefのテンプレート版とも言える。



.. code-block:: c++
  
  template < typename T >
  struct wrap { } ;
  
  template < typename T >
  using Alias = wrap<T> ;
  
  Alias<int> t1 ; // wrap<int>
  Alias<double> t2 ; // wrap<double>


エイリアステンプレートによって宣言されたテンプレートIDは、エイリアスされた型の別名として使うことができる。エイリアステンプレートのテンプレートIDは、typedef名と同じく、型の別名であり、別の型ではない。Alias&lt;int&gt;は、wrap&lt;int&gt;と同一の型である。



エイリアステンプレートの利用例を挙げる。



.. code-block:: c++
  
  template < typename T, typename U >
  struct wrap
  {
      using type = T ;
  } ;
  
  template < typename T >
  using a1 = wrap< T, int > ;
  using t1 = a1<int> ; // wrap< int, int >
  
  template < typename T >
  using a2 = wrap< T, T > ;
  using t2 = a2< int > ; // wrap< int, int >
  
  template < typename T >
  using a3 = typename wrap< T, void >::type ;
  using t3 = a3<int> ; // wrap< int, void>::type、すなわちint


エイリアステンプレートは、その利用方法はさておき、以下のような記述もできる。



.. code-block:: c++
  
  template < typename T >
  using a1 = T ; // a1<T>はTの別名
  
  template < typename T >
  using a2 = int ; // a2<T>はintの別名


エイリアステンプレートは、テンプレート実引数の一部のみ指定し、残りをテンプレート化することができる。その利用方法は、例えば、カスタムアロケーターを指定したコンテナーテンプレートの別名を宣言できる。



.. code-block:: c++
  
  class MyAlloc ;
  
  template < typename T >
  using MyVec = std::vector< T, MyAlloc > ;


従来のtypedef宣言では、これができない。



エイリアステンプレートは、名前通りテンプレートであるので、名前空間スコープかクラススコープの内側でしか宣言できない。たとえば、関数のブロックスコープの内側では宣言できない。



.. code-block:: c++
  
  void f()
  {// 関数のブロックスコープ
      template < typename T > using A = T : // エラー
  }


エイリアステンプレート宣言内のテンプレートIDは、宣言中のエイリアステンプレートを参照してはならない。つまり、宣言中に自分自身の特殊化を使ってはならないという事である。



.. code-block:: c++
  
  template < typename T > struct A ;
  template < typename T > using B = typename A<T>::U;
  template < typename T > struct A
  {
      typedef B<T> U;
  } ;
  
  // エラー、B<int>の実体化の際に、A<int>::Uとして、自分自身を使ってしまう。
  B<int> b;




名前解決(Name Resolution)
--------------------------------------------------------------------------------



テンプレート定義内での名前解決は非常に複雑である。これは、テンプレートはある場所で宣言され、別の場所で特殊な形に実体化されるからである。



テンプレート定義内では、三種類の名前がある。



* テンプレート自身の名前、テンプレートで宣言された名前
* テンプレート仮引数に依存する名前
* テンプレート定義のあるスコープから見える名前


「テンプレート自身の名前、テンプレートで宣言された名前」というのは、テンプレート名と、テンプレート仮引数名である。



「テンプレート仮引数に依存する名前」は、依存名(Dependent Name)と呼ばれている。



「テンプレート定義のあるスコープから見える名前」とは、テンプレート定義のあるスコープやその外側のスコープで、すでに宣言された名前のことだ。



テンプレート仮引数に依存する名前は、暗黙に型を意味しないものと解釈される。



.. code-block:: c++
  
  template < typename T >
  void f()
  {
      int x = T::value ; // T::valueは型ではない
  }


この場合、Tに与えられるテンプレート実引数には、例えば以下のようなものが想定されている。



.. code-block:: c++
  
  struct X
  {
      static constexpr int value = 0 ;
  } ;


テンプレート宣言や定義で、テンプレート仮引数に依存する名前を型として使おうとしてもエラーとなる。なぜならば、すでに述べたように、暗黙に型を意味しないものと解釈されるからだ。



template &lt; typename T &gt;
void f()
{
    typedef T::type type ; // エラー、T::typeは型ではない
}



依存名を型であると解釈させるには、明示的に、名前の直前に、typenameキーワードを記述して修飾しなければならない。



.. code-block:: c++
  
  template < typename T >
  void f()
  {
      typedef typename T::type type ; // OK、T::typeは型
  }


ただし、メンバー初期化子と基本クラス指定子には、文法上型しか記述できないので、typenameで修飾する必要はない。



.. code-block:: c++
  
  template < typename T >
  struct X : T::type // OK
  {
      X() : T::type // OK
      { } 
  } ;


また、メンバーテンプレートは、文脈により、テンプレートかどうかが曖昧になる。



.. code-block:: c++
  
  // Tに渡す型の例
  struct X
  {
      template < typename T >
      void func() ;
  } ;
  
  template < typename T >
  void f()
  {
      T t ;
      t.func<int>(0) ; // エラー
  }


このコードの意味は、t.funcとintに、比較演算子である&lt;を適用し、さらに比較演算子&gt;とかっこに囲まれた0を適用するものである。メンバー関数テンプレートの特殊化を呼び出すものではない。
t.funcとintを&lt;演算子で比較するのは、文法上認められていないので、このコードはエラーになる。



依存名に.や-&gt;、あるいは::を用い、メンバーテンプレートの特殊化を記述する場合は、メンバーテンプレートは、templateキーワードで修飾しなければならない。これは、メンバー名がテンプレートであると明示的に解釈させるためである。



.. code-block:: c++
  
  // Tに渡す型の例
  struct X
  {
      template < typename T >
      struct MemberClass ;
  
      template < typename T >
      void MemberFunction() ;
  } ;
  
  template < typename T >
  void f()
  {
      typedef typename T:: template MemberClass<int> obj ;
  
      T t ;
      t. template MemberFunction<int>() ;
  
      T * p = &t ;
      p-> template MemberFunction<int>() ;
  }


これはメンバーテンプレートの特殊化を使う場合であって、メンバー関数テンプレートを実引数推定させて使う場合には、templateキーワードを記述する必要はない。



.. code-block:: c++
  
  // Tに渡す型の例
  struct X
  {
      template < typename T >
      void MemberFunction( T ) ;
  } ;
  
  template < typename T >
  void f()
  {
      T t ;
      t.MemberFunction( 0 ) ; // OK
  }


templateキーワードの指定は、実際には文法の曖昧性の問題であって、名前解決の問題ではないのだが、typenameキーワードの指定と似ているために、便宜上、本書では同時に説明することにした



依存(Dependent)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



依存(Dependent)とは、テンプレート仮引数に依存することである。テンプレート仮引数に依存するものは、名前と式とテンプレート実引数である。式とテンプレート実引数には、型依存式と値依存式が存在する。



なぜテンプレート仮引数に依存しているかどうかが問題になるのか。テンプレート仮引数というのは、具体的な内容が確定していない存在だからだ。テンプレートは、実体化されて初めて、その具体的な内容が確定する。



依存の詳細は煩雑になるので省略するが、簡略化していえば、テンプレート仮引数が関わる名前や式は、すべて依存している。




.. code-block:: c++
  
  void f( int ) ;
  
  template < typename T >
  struct identity
  {
      using type = T ;
  } ;
  
  template < typename T >
  struct X
  {
      int data ;
  
      void member()
      {
          T t1 ; // Tは依存名
          T::value ; // 依存している。値と解釈される
          typename T::type t2 ; // 依存している。型と解釈される
  
          f( 0 ) ; // 依存していない
  
          &X::data ; // 依存している
          this->data ; / 依存している
  
          typename identity<T>::type t ; // 依存している
      } 
  } ;


クラステンプレートの場合、クラス名やthisを介した式も、テンプレート仮引数に依存している。なぜならば、クラステンプレートの場合、クラス名自体がテンプレート仮引数に依存しているからだ。



依存していない名前や式を、非依存(Non-dependent)という。





非依存名の名前解決
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



非依存名は、テンプレートが定義されている場所で名前解決される。



.. code-block:: c++
  
  void f( int ) ;
  
  
  template < typename T >
  void g()
  {
      f( 0 ) ; // f(int)
  }
  
  void f( double ) ;
  
  
  int main()
  {
      g<int>() ;
  
  }


このコードの解釈は驚くにあたらない。ただし、状況によっては、意図しないことが起こる。



.. code-block:: c++
  
  // Derivedのテンプレート仮引数Baseが想定している型
  struct Base
  {
      void member() { }
  } ;
  
  
  template < typename Base >
  struct Derived : Base
  {
      void f()
      {
          member() ; // エラー、memberが見つからない
      }
  
  } ;


この、テンプレートクラス、Derivedは、テンプレート仮引数を基本クラスに指定している。そして、基本クラスはmemberという名前のメンバー関数を持っていることを期待している。Derived::f内で使われている、memberという名前は、非依存名であり、しかも非修飾名なので、メンバー関数であるとは解釈されない。そのため、外側のスコープのmemberという名前を探すが、見つからないためエラーになる。



このようなコードで、memberをメンバーとして扱いたい場合、memberを修飾して依存名にする必要がある。それには、三種類の方法がある。



.. code-block:: c++
  
  template < typename Base >
  struct Derived : Base
  {
      void f()
      {
          Derived::member() ; // OK、クラス名は依存名
          this->member() ; // OK、thisは依存式
          Base::member() ; // OK、テンプレート仮引数は依存名
      }
  
  } ;




依存名の名前解決
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



依存名の名前解決は、実体化場所(Point of Instantiation)が重要になる。



実体化場所とは、テンプレートが実体化された場所のことである。



template &lt; typename T &gt;
void f( T ) { } // テンプレートの定義

struct Foo { } ;

int main()
{
    Foo foo ;
    f( foo ) ; // 実体化場所
}



依存名の名前解決は、テンプレートの定義ではなく、実体化場所で行われるので、テンプレートの定義の時点では見えていない、Fooという名前も使うことができる。また、テンプレートの定義中で、テンプレート仮引数のメンバー名やネストされた型名を参照しても、実体化の結果が一致しているならば、名前解決できる。



テンプレートの名前解決の理解を難しくしているのは、オーバーロード解決における、候補関数の見え方である。



非修飾名前解決と修飾名前解決を使った候補関数は、テンプレートの定義場所から見える名前のみに制限される。



.. code-block:: c++
  
  void f( int ) { }
  
  // テンプレートの定義
  template < typename T >
  void call( )
  {
      f( 0.0 ) ; // 候補関数はf(int)のみ
  } 
  
  void f( double ) { }
  
  int main()
  {
      call<void>() ; // 実体化場所
  }


このように、候補関数の非修飾名前解決と修飾名前解決は、実体化場所で行われるものの、発見される名前は、テンプレートの定義場所から見える名前のみに限定されているため、。上記の例では、もし、f(double)が候補関数に含まれていたならば、そちらが最適関数だが、候補関数として発見されないために、最適関数になることもない。



同様に、以下の例はエラーとなる。



.. code-block:: c++
  
  // テンプレートの定義
  template < typename T >
  void call( )
  {
      f( 0 ) ; // エラー、名前fが見つからない
  } 
  
  void f( int ) { }
  
  int main()
  {
      call<void>() ; // 実体化場所
  }


ただし、ADLの場合は、例外的に異なる。ADLが発動した場合は、テンプレートの実体化場所から見える候補関数が発見される。



.. code-block:: c++
  
  // グローバル名前空間
  
  // クラスFooの関連名前空間はグローバル名前空間
  struct Foo { } ;
  
  // テンプレートの定義
  template < typename T >
  void call_f( T t )
  {
      f( t ) ;
  } 
  
  // グローバル名前空間内の名前
  void f( Foo ) { }
  
  int main()
  {
      Foo foo ;
      call_f( foo ) ; // OK、ADLが発動
  }


この場合、関数call_f内で呼び出している非修飾名fは、非修飾名前解決では見つからないため、ADLが発動する。



これはADLが発動する場合のみの例外的なルールである。ADLが発動しない場合は、このような例外的な挙動にはならない。



.. code-block:: c++
  
  struct Foo { } ;
  
  void f( Foo const & ) { } // #1
  
  template < typename T >
  void call_f( T t )
  {
      f( t ) ;
  } 
  
  void f( Foo & ) { } // #2
  
  int main()
  {
      Foo foo ;
      call_f( foo ) ; // ADLは発動しない。#1が呼ばれる
  }


この場合では、非修飾名前解決により、#1が、名前fとして見つかるため、ADLは発動しない。ADLが発動しないので、#2が候補関数に選ばれることもない。もし、#2が候補関数に選ばれていたならば、オーバーロード解決により、#2は#1より最適な関数となるが、ADLが発動しない以上、#2は発見されず、したがって候補関数にもならない。



また、基本型には、関連名前空間が存在しないため、ADLは発動しない。



このように、テンプレート内の名前は、テンプレートの定義場所と、実体化場所で、二段階に分けて名前解決されるので、二段階名前解決(Two Phase Lookup)と呼ばれている。





テンプレートの実体化と特殊化(Template instantiation and specialization)
--------------------------------------------------------------------------------



テンプレートは、テンプレート実引数を与えられて実体化して始めて利用可能になる。これをテンプレート実体化(template instantiation)という。実体化には、暗黙の実体化と明示的な実体化がある。実体化したテンプレートのことを、特殊化(specialization)という。特殊化は、明示的に行うこともできる。テンプレートの部分的特殊化は、名前が似ているが、いまだにテンプレートであって、実体化された特殊化ではない。



暗黙の実体化(Implicit instantiation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



明示的に実体化されず、明示的に特殊化されていないテンプレートは、オブジェクトの完全な型が必要な場合や、クラス型が完全であることがプログラムの意味に影響を与える文脈で参照された場合に、暗黙に実体化される。



クラステンプレートが暗黙に実体化されても、クラステンプレートのメンバーまで暗黙に実体化されるわけではない。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() ;
      void g() ;
  } ;
  
  
  int main()
  {
      typedef X< int > type ; //  X<int>の実体化は必要ない
      type a ; // X<int>の実体化が必要
      X< char > * b ; // X<char>の実体化は必要ない
      X< double > * p ; // X<double>の実体化は必要ない
  
      a.f() ; // X<int>::f()の実体化が必要
      b->f() ; // X<char>::f()の実体化が必要
  }


typedef名やポインター型の宣言は、クラスの完全な型が必要な文脈ではないので、テンプレートの暗黙の実体化は起こらない。


X&lt;char&gt;や X&lt;double&gt;の実体化が必要ないのは、クラスへのポインターを参照しているだけなので、クラスの完全な型が必要な文脈ではないからである。また、X&lt;int&gt;::g()やX&lt;double&gt;::g()も、参照されていないので実体化はされない。



関数テンプレートも、定義が必要な文脈で参照されなければ、暗黙に実体化されることはない。



実体化の必要のないクラステンプレートのメンバーが暗黙的に実体化されないという挙動は、規格上保証されている。



テンプレートが暗黙に実体化される場合、暗黙的な実体化が必要ない場合、また例外的に暗黙的に実体化されるかどうかが未規定の場合の詳細な解説は、煩雑になるので省略する。






明示的実体化(Explicit instantiation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



クラス、関数、メンバーテンプレートの特殊化は、テンプレートから明示的に実体化できる。メンバー関数、メンバークラス、クラステンプレートのstaticデータメンバーは、クラステンプレートのメンバーの定義として、明示的に実体化できる。これを明示的実体化(Explicit instantiation)という。



明示的実体化を宣言する文法は、以下の通りである。



.. code-block:: c++
  
  exte

externキーワードは省略できる。externキーワードの有無に意味上の違いはない。C++03までの規格では、externキーワードを使った文法は、明示的実体化の宣言ではなく、内部リンケージの宣言になり、プログラムの意味が変わってしまうので、注意が必要である。本書はC++11の規格のみを取り扱う。



クラス、もしくはメンバークラスに対する明示的実体化の場合、宣言中のクラス名はテンプレート実引数を指定した形で指定する。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  // X<int>の明示的実体化
  extern template struct X< int > ;


externキーワードは省略できるので、上記の明示的実体化は、以下のように書くこともできる。



.. code-block:: c++
  
  template struct X< int > ;


関数、もしくはメンバー関数に対する明示的実体化の場合、宣言中の関数名は、テンプレート実引数を指定しているか、引数リストからテンプレート実引数が推定できる形で指定する。




.. code-block:: c++
  
  template < typename T >
  void f( T ) { }
  
  // f<int>の明示的実体化
  extern template void f< int >( int ) ;
  
  template < typename T >
  void g( T ) { }
  
  // g<int>の明示的実体化
  extern template void g( int ) ;
  // 以下と同等
  // extern template void g< int >( int ) ;


クラスのメンバーに対する明示的実体化の場合は、メンバーの属するクラス名はテンプレート実引数を指定した形で指定する。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() { }
  } ;
  
  extern template void X<int>::f() ;


同じテンプレートとテンプレート実引数に対する明示的実体化は、プログラム中に一度しか現れてはならない。つまり、複数のソースファイルからなるプログラム全体でも、一度しか現れてはならない。規格上、実装はこの違反を検出できるよう規定されてはいないので、実装の出力するコンパイル時、実行時のエラーや警告のメッセージに頼ることは出来ない。




関数テンプレート、メンバー関数、クラステンプレートのstaticデータメンバーは、明示的実体化の前に宣言されていなければならない。



.. code-block:: c++
  
  // エラー、前方に宣言がない
  extern template void f<int>() ;
  
  template < typename T > void f() ;


クラステンプレート、クラステンプレートのメンバークラス、メンバークラステンプレートは、明示的実体化の前に定義されていなければならない。



.. code-block:: c++
  
  template < typename T >
  struct X ; // 宣言
  
  // エラー、クラステンプレートXは前方で定義されていない
  extern template struct X<int> ;
  
  template < typename T >
  struct X { } ; // 定義


明示的実体化で、暗黙に宣言された特別なメンバー関数を指定した場合、エラーとなる。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  // エラー、暗黙に宣言されたコンストラクター
  extern template X<int>::X() ;
  
  template < typename T >
  struct Y
  {
      Y() { } // 明示的な宣言
  } ;
  
  // OK
  extern template Y<int>::Y() ; 


同じテンプレート実引数の明示的特殊化の宣言の後に明示的実体化の宣言が現れた場合、明示的実体化は無効となる。これはエラーではない。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  // X<int>に対する明示的特殊化
  template < >
  struct X<int> { } ;
  
  // X<int>に対する明示的実体化。
  // 無効、エラーではない
  extern template struct X<int> ;


同じテンプレート実引数に対する明示的特殊化の前に明示的実体化が現れた場合はエラーである。



明示的実体化を使えば、プログラム中のテンプレートを必要とするソースファイルすべてにトークン列が一致するテンプレートの完全な定義を持ち込む必要がなくなる。



.. code-block:: c++
  
  // func.h
  // 関数テンプレートfuncの宣言
  template < typename T >
  void func( T ) ;


.. code-block:: c++
  
  // func.cpp
  // 関数テンプレートfuncの定義
  #include <func.h>
  
  template < typename T >
  void func( T ) { }
  
  // プログラム中で使われる実体化を明示的に宣言
  extern template void func( int ) ;
  extern template void func( double ) ;


.. code-block:: c++
  
  // main.cpp
  
  // このソースファイルmain.cppには、
  // 関数テンプレートfuncの宣言のみ導入
  #include <func.h>
  
  int main()
  {
      func( 0 ) ; // OK、プログラム中で明示的実体化されている
      func( 0.0 ) ; // OK、プログラム中で明示的実体化されている
  
      func ( 'a' ) ; // エラー、定義がないため、実体化できない。
  }


C++におけるテンプレートは、トークン列が一致するコード片を、テンプレートの特殊化を必要とするプログラム中のソースファイルすべてに持ち込むことで、ODRを例外的に回避している。明示的実体化を使えば、テンプレートの宣言と定義を分離し、すべてのソースファイルに定義を持ち込む必要がなくなる。ただし、明示的に実体化したテンプレートとそのテンプレート実引数に限定される。





明示的特殊化(Explicit specialization)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



テンプレートはあるテンプレート実引数について、元となるテンプレートとは別に、明示的に特殊化することができる。これを明示的特殊化(Explicit specialization)という。明示的特殊化を使うと、ある与えられたテンプレート実引数に対しては、汎用のテンプレートから実体化される特殊化は異なる特殊化を与えることができる。明示的特殊化と、部分的特殊化は、名前は似ているは全くの別物である。



明示的特殊化の文法は以下の通り。



.. code-block:: c++
  
  template < > 宣言


.. code-block:: c++
  
  template < typename T >
  bool f( T ) { return false ; }
  
  // 明示的特殊化
  template < >
  bool f( int ) { return true ; }
  
  int main()
  {
      f( 0 ) ; // true
      f( 0.0 ) ; // false
      f( 'a' ) ; // false
  }


この例では、関数テンプレートfにテンプレート実引数intを与えた場合だけ、元のテンプレート定義とは別の、明示的特殊化による定義を使用する。そのため、f&lt;int&gt;はtrueを返す。



明示的特殊化は、元のテンプレートの定義の影響を受けない。たとえば、関数テンプレートの場合は戻り値の型を異なるものにできるし、クラステンプレートの場合、クラスのメンバーを全く違ったものにすることもできる。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() { }
  } ;
  
  template < >
  struct X<int>
  {
      void g() ;
  }


この例では、元のテンプレートの定義であるメンバー関数X::fがなく、全く別名のメンバー関数gを定義している。



明示的特殊化できるテンプレートは、以下の通り。



* 
  関数テンプレート



  .. code-block:: c++  
    
    template < typename T >
    void f( T ) { }
    
    // 明示的特殊化
    template < >
    bool f( int ) { return true ; }
    
    // 明示的なテンプレート実引数の指定によるもの
    template < >
    void f<short>( short ) { }
  


* 
  
クラステンプレート



  .. code-block:: c++  
    
    template < typename T >
    struct X { } ;
    
    // 明示的特殊化
    template < >
    struct X<int>
    {
        int data ;
    } ;
  


* 
  
クラステンプレートのメンバー関数



  .. code-block:: c++  
    
    template < typename T >
    struct X
    {
        void f() { }
        void g() { }
        int data ;
    } ;
    
    // ひとつのメンバー関数のみを明示的特殊化
    template < >
    bool X<int>::f() { return true ; }
  

  
クラステンプレートのメンバー関数を個別に明示的特殊化することができる。この場合、クラステンプレートXにテンプレート実引数intを与えて実体化させた特殊化は、X::fのみ明示的特殊化の定義を使い、残りのメンバーはテンプレートから実体化された特殊化を使う。




* 
  
クラステンプレートのstaticデータメンバー



  .. code-block:: c++  
    
    template < typename T >
    struct X
    {
        static int data ; // 宣言
    } ;
    
    template < typename T >
    int X<T>::data ; // 定義
    
    // 明示的特殊化
    template < >
    int X<int>::data ;
  

  
クラステンプレートのstaticデータメンバーの明示的特殊化は、宣言の型を変えることはできない。



  .. code-block:: c++  
    
    template < typename T >
    struct X
    {
        static int d1 ;
        static T d2 ;
    } ;
    
    // 汎用的な定義
    template < typename T >
    int X<T>::data = 0 ;
    
    
    template < >
    double X<int>::d1 ; // エラー、型が宣言と一致しない
    
    template < >
    double X<int>::d2 ; // エラー、型が宣言と一致しない
  

  
ただし、初期化式を変えることはできる。



  .. code-block:: c++  
    
    template < typename T >
    struct X
    {
        static int data ;
    } ;
    
    template < typename T >
    int X<T>::data = 0 ;
    
    template < >
    int X<int>::data = 1 ;
    
    template < >
    int X<double>::data = 2 ;
  


* 
  
クラステンプレートのメンバークラス



  .. code-block:: c++  
    
    template < typename T >
    struct Outer
    {
        struct Inner { /* 定義 */ } ;
    } ;
    
    // 明示的特殊化
    template < >
    struct Outer<int>::Inner
    {
    // 定義
    } ;
  


* 
  
クラステンプレートのメンバーenum



  .. code-block:: c++  
    
    template < typename T >
    struct X
    {
        enum struct E { foo, bar } ;
    } ;
    
    // 明示的特殊化
    template < >
    enum struct X<int>::E
    {
        hoge, moke
    } ;
  


* 
  
クラス、あるいはクラステンプレートのメンバークラステンプレート



  .. code-block:: c++  
    
    // クラス
    struct Outer_class
    {
        template < typename T >
        struct Inner_class_template { } ;
    } ;
    
    // 明示的特殊化
    template < >
    struct Outer_class::Inner_class_template<int>
    {
    // 定義
    } ;
    
    // クラステンプレート
    template < typename T >
    struct Outer_class_template
    {
        template < typename U >
        struct Inner_class_template { } ;
    } ;
    
    // 明示的特殊化
    template < > // Outer_class_templateの明示的特殊化
    template < > // Inner_class_templateの明示的特殊化
    struct Outer_class_template<int>::Inner_class_template<int>
    {
    // 定義
    } ;
  

  
クラス、クラステンプレートを問わず、メンバークラステンプレートの明示的特殊化ができる。



* 
  
クラス、あるいはクラステンプレートのメンバー関数テンプレート



  .. code-block:: c++  
    
    // クラス
    struct Outer_class
    {
        template < typename T >
        void member_function_template() { }
    } ;
    
    // 明示的特殊化
    template < >// クラス
    struct Outer_class
    {
        template < typename T >
        void member_function_template() { }
    } ;
    
    // メンバー関数テンプレートの明示的特殊化
    template < >
    void Outer_class::member_function_template<int>()
    {
    // 定義
    }
    
    
    // クラステンプレート
    template < typename T >
    struct Outer_class_template
    {
        template < typename U >
        void member_function_template() { }
    } ;
    
    // メンバー関数テンプレートの明示的特殊化
    template < > // Outer_class_templateの明示的特殊化
    template < > // member_function_templateの明示的特殊化
    void Outer_class_template<int>::member_function_template<int>()
    {
    // 定義
    }
  




テンプレートの明示的特殊化は、修飾名の場合、テンプレートの宣言されている名前空間の外側で宣言することもできる。



.. code-block:: c++
  
  namespace ns {
  
  template < typename T >
  void f( T ) { }
  }
  
  // ns::fの明示的特殊化
  template < >
  void ns::f( int ) { }


関数テンプレートとクラステンプレートの場合、明示的特殊化の元となるテンプレートの宣言は、明示的特殊化の宣言より先行していなければならない。



.. code-block:: c++
  
  // エラー、テンプレートの宣言が先行していない
  template < >
  void f( int ) ; 
  
  // テンプレートの宣言
  template < typename T >
  void f( T ) ;
  
  // OK、テンプレートの宣言が先行している
  template < >
  void f( short ) ;


メンバーテンプレートに対する明示的特殊化の定義には、メンバーの属するクラスもしくはクラステンプレートの定義が先行していなければならない。



.. code-block:: c++
  
  // クラスの宣言
  struct Outer ;
  
  // エラー、クラスの定義が先行していない
  template < >
  struct Outer::Inner<int> { } ;
  
  // クラスの定義
  struct Outer
  {
      // メンバーテンプレート
      template < typename T >
      struct Inner { } ;
  } ;
  
  // OK、クラスの定義が先行している
  template < >
  struct OUter::Inner<short> { } ;


メンバー関数、メンバー関数テンプレート、メンバークラス、メンバーenum、メンバークラステンプレート、クラステンプレートのstaticデータメンバーは、暗黙に実体化されるクラスの特殊化に対しても、明示的に特殊化できる。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() { }
      void g() { }
  } ;
  
  // X<int>::fの明示的特殊化
  template < >
  void X<int>::f() { }
  
  
  int main()
  {
      X<int> x ; // X<int>を暗黙的に実体化
      x.f() ; // 明示的特殊化を使う
      x.g() ; // 暗黙に実体化された特殊化を使う
  }


このように、一部のメンバーだけを明示的に特殊化できる。明示的に特殊化されなかったメンバーが使われた場合は、クラステンプレートから暗黙の実体化による特殊化が使われる。



メンバーの明示的特殊化より、クラステンプレートの定義が先行していなければならない。



.. code-block:: c++
  
  // エラー
  template < >
  void X<int>::f() { }
  
  template < typename T >
  struct X
  {
      void f() { }
  } ;


暗黙に宣言される特別なメンバー関数を明示的特殊化することはできない。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
  // デフォルトコンストラクタ―は暗黙に宣言される
  } ;
  
  // エラー
  // 暗黙に宣言される特別なメンバー関数の明示的特殊化
  template < >
  X<int>::X() { }
  
  template < typename T >
  struct Y
  {
      Y() { } // 特別なメンバー関数の明示的な宣言
  } ;
  
  // OK
  // 暗黙に宣言されていない特別なメンバー関数の明示的特殊化
  template < >
  Y<int>::Y() { }


このように、特別なメンバー関数を明示的特殊化する場合には、クラステンプレートの定義内で、明示的に宣言する必要がある。



明示的特殊化されたクラステンプレートのメンバーは、元のクラステンプレートとは独立して存在する。そのため、元のクラステンプレートとは全く違うメンバーの宣言にすることができる。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() ;
  } ;
  
  // 明示的特殊化
  template < >
  struct X<int>
  { // 元のクラステンプレートとは違うメンバー
      void g() ;
  } ;


明示的特殊化されたクラステンプレートの定義内のメンバー宣言は、通常のクラス定義のように記述する。つまり、template &lt; &gt;をつける必要はない。メンバーの定義をクラス定義の外に記述する場合も同じ。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  // 明示的特殊化されたクラステンプレート
  template < >
  struct X<int>
  {
      void f() ; // 宣言
  } ;
  
  // 明示的特殊化されたクラステンプレート定義のメンバーの定義
  // template < >は必要ない
  void X<int>::f() { }


ただし、明示的に特殊化されたメンバークラステンプレートのメンバーを定義するときには、template &lt; &gt;が必要である。メンバークラスではなく、メンバークラステンプレートであることに注意。



.. code-block:: c++
  
  template < typename T >
  struct Outer
  {
      // メンバークラス
      struct Inner { } ;
  
      // メンバークラステンプレート
      template < typename U >
      struct Inner_temp { } ;
  } ;
  
  // 特殊化Outer<int>のメンバークラスの明示的特殊化
  template < >
  struct Outer<int>::Inner
  {
      void f() ;
  } ;
  
  // メンバークラスのメンバーの定義
  // template < >は必要ない
  void Outer<int>::Inner::f() { }
  
  // 特殊化Outer<int>のメンバークラステンプレートの明示的特殊化
  template < >
  template < typename U >
  struct Outer<int>::Inner_temp
  {
      void f() ;
  } ;
  
  // メンバークラステンプレートのメンバーの定義
  // template < >が必要
  template < >
  template < typename U >
  void Outer<int>::Inner_temp<U>::f() { }


テンプレート、メンバーテンプレート、クラステンプレートのメンバーが明示的に特殊化されている場合、暗黙の実体化が起こる前に、明示的特殊化が宣言されていなければならない。



.. code-block:: c++
  
  template < typename T >
  struct X
  { } ;
  
  // テンプレートの特殊化X<int>の使用
  // X<int>に対する暗黙の実体化が起こる。
  X<int> i ;
  
  // エラー、明示的特殊化の宣言より前に、特殊化の暗黙の実体化が起こっている。
  template < >
  struct X<int> { } ;


テンプレートの明示的特殊化の名前空間スコープは、テンプレートの名前空間スコープと同じ。



宣言されているが定義されていない明示的特殊化を指すテンプレート名は、不完全定義されたクラスと同様に使うことができる。



.. code-block:: c++
  
  template < typename T >
  struct X { } ;
  
  // 明示的特殊化の宣言
  // X<int>はまだ定義されていない
  template < >
  struct X<int> ;
  
  X<int> * p ; // OK、不完全型へのポインター
  X<int> obj ; // エラー、不完全型のオブジェクト


関数テンプレートの明示的特殊化の際のテンプレート名のテンプレート引数は、テンプレート実引数の型が、関数の実引数の型から推定できる場合は、省略することができる。



.. code-block:: c++
  
  template < typename T > struct X { } ;
  
  template < typename T >
  void f( X<T> ) ;
  
  // 関数テンプレートf<int>の明示的特殊化
  // テンプレートの特殊化の型は実引数の型から推定可能
  template < >
  void f( X<int> ) { }


ある関数テンプレートと同じ名前で、関数テンプレートの特殊化と同じ型の関数であっても、その関数は、関数テンプレートの明示的特殊化ではない。



.. code-block:: c++
  
  // 関数テンプレートf
  template < typename T >
  void f( T ) { }
  
  // 関数テンプレートfの明示的特殊化f<int>
  template < >
  void f( int ) { }
  
  // 関数f
  // 関数テンプレートfの明示的特殊化ではない
  void f( int ) { }


関数テンプレートの明示的特殊化は、宣言にinline指定子があるか、deleted定義されている場合のみ、inlineとなる。元の関数テンプレートのinline指定子の有無には影響されない。



.. code-block:: c++
  
  // inline指定子のある関数テンプレート
  template < typename T >
  inline void f( T ) { }
  
  // 非inline関数
  // 元のテンプレートのinline指定子には影響されない
  template < >
  void f( int ) { }
  
  // inline関数
  template < >
  inline void f( short ) { }


テンプレートのstaticデータメンバーの明示的特殊化の宣言は、初期化子を含む場合、定義となる。初期化子を含まない場合は宣言となる。デフォルト初期化が必要なstaticデータメンバーを定義する場合は、文法上の制約から、初期化リストを使う必要がある。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      static int data ;
  } ;
  
  // 明示的特殊化の宣言、定義ではない
  template < >
  int X<int>::data ; 
  
  // エラー、メンバー関数int ()の宣言
  // 文法上の制約による
  template < >
  int X<int>::data () ;
  
  // 明示的特殊化の定義
  template < >
  int X<int>::data { } ;


クラステンプレートのメンバーとメンバーテンプレートは、クラステンプレートで定義されていて、クラステンプレートが暗黙に実体化されていても、明示的特殊化できる。



.. code-block:: c++
  
  template < typename T >
  struct X
  {
      void f() { } 
      void g() { }
  } ;
  
  // 明示的特殊化
  template < >
  void X<int>::f() { }
  
  int main()
  {
      X<int> x ; // X<int>の暗黙の実体化
      x.f() ; // 明示的特殊化が使われる
      x.g() ; // 暗黙の実体化により生成された特殊化が使われる
  }


これにより、メンバーやメンバーテンプレートの一部だけを明示的に特殊化することができる。



ネストしたクラステンプレートのメンバーやメンバーテンプレートを明示的特殊化する場合、ネストした数だけtemplate&lt;&gt;を記述する必要がある。



.. code-block:: c++
  
  template < typename T1 >
  struct Outer
  {
      template < typename T2 >
      struct Inner
      {
          template < typename T3 >
          void f() { }
      } ;
  } ;
  
  template < > // Outer<int>の明示的特殊化
  template < > // Outer<int>::Inner<int>の明示的特殊化
  template < > // Outer<int>::Inner<int>::f<int>の明示的特殊化
  void Outer<int>::Inner<int>::f<int>( ) { }




関数テンプレートの特殊化(Function template specializations)
--------------------------------------------------------------------------------



<p class="todo">
partial orderingの解説。


