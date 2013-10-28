例外(Exception handling)
================================================================================

例外を投げる(Throwing an exception)
--------------------------------------------------------------------------------



例外を投げる(throwing an exception)とは、日本語では他にも、送出するとかスローするなどとも書かれている。



例外を投げると、処理はハンドラーに移る。例外を投げるときには、オブジェクトが渡される。オブジェクトの型によって、処理が渡されるハンドラーが決まる



.. code-block:: c++
  
  // int型
  throw 0 ;
  
  // const char *型
  throw "hello" ;
  
  struct X { } ;
  X x ;
  // X型
  throw x ; 


例外が投げられると、型が一致する最も近い場所にあるハンドラーに処理が移る。「最も近い」というのは、最近に入って、まだ抜けていないtryブロックに対応するハンドラーである。



.. code-block:: c++
  
  // 例外を投げる
  void f() { throw 0 ; }
  
  int main()
  {
      try
      {
          try
          {
              try { f() } // 関数fの中で例外を投げる
              catch( ... ) { } // ここに処理が移る
          }
          catch( ... ) { }
      }
      catch( ... ) { }
  }


throw式はオペランドから一時オブジェクトを初期化する。この一時オブジェクトを例外オブジェクト(exception object)という。例外オブジェクトの型を決定するには、throw式のオペランドの型からトップレベルのCV修飾子を取り除き、T型への配列型はTへのポインター型へ、T型を返す関数型は、T型を返す関数へのポインター型に変換する。



.. code-block:: c++
  
  throw 0 ; // int
  
  int const a = 0 ;
  throw a ; // int
  
  int const volatile * const volatile p = &a ;
  throw p ; // int const volatile *
  
  int b[5] ;
  throw b ; // int *
  
  int f( int ) ;
  throw f ; // int (*)(int)


この一時オブジェクトはlvalueであり、型が適合するハンドラーの変数の初期化に使われる。



.. code-block:: c++
  
  void f()
  {
      try
      {
          throw 0 ; // 例外オブジェクトはint型のlvalue
      }
      catch( int exception_object ) // 例外オブジェクトで初期化される
      { }
  }


例外オブジェクトの型が不完全型か不完全型へのポインター型である場合は、エラーとなる。



.. code-block:: c++
  
  struct incomplete_type ;
  
  void f()
  {
      // エラー、不完全型へのポインター型
      throw static_cast<incomplete_type *>(nullptr) ;
  }


ただし、void型はその限りではない。



.. code-block:: c++
  
  void f()
  {
      // OK、void *
      throw static_cast<void *>(nullptr) ;
  }


いくつかの制限を除けば、throw式のオペランドは、関数への実引数やreturn文のオペランドとほぼ同じ扱いになっている。



例外オブジェクトのメモリーは、未規定の方法で確保される。



例外オブジェクトの寿命の決定にはふたつの条件があり、どちらか遅い方に合わせて破棄される。



ひとつは例外を再び投げる以外の方法で、例外を捉えたハンドラーから抜け出すこと。



.. code-block:: c++
  
  void f()
  {
  
      try
      {
          throw 0 ;
      }
      catch ( ... )
      {
      // return文やgoto文などでハンドラーの複合分の外側に移動するか
      // あるいはハンドラーの複合分を最後まで処理が到達すれば、例外オブジェクトは破棄される
      }
  
  }


例外が再び投げられた場合は、例外オブジェクトの寿命は延長される。



.. code-block:: c++
  
  void f() ; // 例外を投げるかもしれない関数
  
  void g() {
  
      try { f() ; }
      catch ( ... ) 
      {
          throw ; // 例外を再び投げる
      }
  }


この場合、例外オブジェクトは破棄されずに、例外処理が続行する。



もうひとつの条件は、例外オブジェクトを参照する最後のstd::exception_ptrが破棄された場合。これはライブラリの話になるので、本書ではstd::exception_ptrについては解説しない。



例外オブジェクトのストレージが解放される方法は未規定である。



例外オブジェクトの型がクラスである場合、クラスのコピーコンストラクターかムーブコンストラクターのどちらか片方と、デストラクターにアクセス可能でなければならない。



以下のようなクラスは、例外オブジェクトとして投げることができる。



.. code-block:: c++
  
  // 例外オブジェクトとして投げられるクラス
  // コピーコンストラクター、ムーブコンストラクター、デストラクターにアクセス可能
  struct throwable1
  {
      throwable1( throwable1 const & ) { }
      throwable1( throwable1 && ) { }
      ~throwable1() { }
  } ;
  
  // 例外オブジェクトとして投げられるクラス
  // コピーコンストラクター、デストラクターにアクセス可能
  
  struct throwable2
  {
      throwable2( throwable2 const & ) { }
      throwable2( throwable2 && ) = delete ;
      ~throwable2() { }
  } ;
  
  // 例外オブジェクトとして投げられるクラス
  //　ムーブコンストラクター、デストラクターにアクセス可能
  struct throwable3
  {
      throwable3( throwable3 const & ) = delete ;
      throwable3( throwable3 && ) { }
      ~throwable3() { }
  } ;


例外オブジェクトとして投げられるクラスの条件を満たすには、コピーコンストラクターとムーブコンストラクターは、どちらか片方だけアクセスできればよい。デストラクターには必ずアクセス可能でなければならない。



以下のようなクラスは投げることができない。



.. code-block:: c++
  
  // 例外オブジェクトとして投げられないクラス
  struct unthrowable
  {
      // コピーコンストラクター、ムーブコンストラクター両方にアクセスできない
      unthrowable( unthrowable const & ) = delete ;
      unthrowable( unthrowable && ) = delete ;
  
      // デストラクターにアクセスできない
      ~unthrowable() = delete ;
  } ;


たとえ、コピーやムーブが省略可能な文脈でも、コピーコンストラクターかムーブコンストラクターのどちらか片方にはアクセス可能という条件を満たしていなければ、クラスは例外オブジェクトとして投げることができない。



例外は、あるハンドラーに処理が移った段階で、とらえられた(キャッチされた)とみなされる。ただし、例外がとらえられたハンドラーから再び投げられた場合は、再びとらえられていない状態に戻る。



.. code-block:: c++
  
  try
  {
      throw 0 ;
  }
  catch( ... )
  {
      // 例外はとらえられた
  
      throw ; // 再びとらえられていない状態に戻る
  }


例外オブジェクトとして投げられる初期化式の評価が完了した後から、例外がとらえられるまでの間に、別の例外が投げられた場合は、std::terminateが呼ばれる。



これが起こるよくある状況は、スタックアンワインディングの最中にデストラクターから例外が投げられることだ.



.. code-block:: c++
  
  // デストラクターが例外を投げるクラス
  struct C
  {
      // デストラクターに明示的な例外指定がない場合、この文脈では暗黙にthrow()になるため
      // デストラクターの外に例外を投げるには例外指定が必要
      ~C() noexcept( false ) { throw 0 ; }
  } ;
  
  int main()
  {
      try 
      {
          C c ;
          throw 0 ;
          // C型のオブジェクトcが破棄される
          // 例外中に例外が投げられたため、std::terminateが呼ばれる
      }
      catch( ... ){ }
  }


一般的に、デストラクターから例外を投げるべきではない。



初期化式の評価が完了した後という点に注意。throw式のオペランドの初期化式の評価中の例外はこの条件に当てはまらない。



.. code-block:: c++
  
  struct X
  {
      X() { throw 0 ; }
  } ;
  
  int main( )
  {
      try
      {
          // OK、初期化式の評価中の例外
          // 例外オブジェクトの型はint
          throw X() ;
      }
      catch( X & exception ) { }
      catch( int exception ) { } // このハンドラーでとらえられる
  }


この例ではX型のオブジェクトを例外としてthrowする前に、初期化中にint型の例外が投げられたので、結果として投げられる例外オブジェクトの型はint型になる。



ただし、初期化式の評価が完了した後という点に注意。初期化完了の後に例外が投げられた場合は、std::terminateが呼ばれる。



.. code-block:: c++
  
  // この例がstd::terminateを呼ぶかどうかは、C++の実装次第である。
  
  struct X
  {
      X( X const & ) { throw 0 ; }
  } ;
  
  int main( )
  {
      try
      {
          // 実装がコピーを省略しない場合、std::terminateが呼ばれる
          // コピーコンストラクターの実行は評価完了後
          throw X() ;
      }
      catch( ... ) { }
  }


この文脈では、賢いC++の実装ならば、コピーを省略できる。ただし、コピーが省略される保証はない。もし、例外オブジェクトを構築する際にコピーが行われたならば、それはthrow式のオペランドの初期化式の評価完了後なので、この条件に当てはまり、std::terminateが呼ばれる。



また、現行の規格の文面にや誤りがあり、以下のコードではstd::terminateが呼ばれるよう解釈できてしまう。



.. code-block:: c++
  
  // 例外によって抜け出す関数
  void f() { throw 0 ; }
  
  struct C
  {
  
      ~C()
      {
          // 例外によって抜け出す関数を呼ぶ
          try { f() ; }
          catch( ... ) { }
      }
  } ;
  
  int main()
  {
      try 
      {
          C c ;
          throw 0 ;
          // 例外がハンドラーにとらえられる前に、cのデストラクターが呼ばれる
      }
      catch( ... ){ }
  }


これは規格の誤りであり、本書執筆の時点で、修正が検討されている。



オペランドのないthrow式は、現在とらえられている例外を再び投げる(rethrow)。これは、最送出とかリスローなどとも呼ばれている。例外が再び有効になり、例外オブジェクトは破棄されずに再利用される。つまり、例外をふたたび投げる際に一時オブジェクトを新たに作ることはない。例外は再びとらえられているものとはみなされなくなり、std::uncaught_exception()の値も、またtrueになる。



.. code-block:: c++
  
  int main()
  {
      try
      {
          try
          {
              throw 0 ;
          }
          catch ( int e )
          { // 例外をとらえる
              throw ; // 一度捉えた例外を再び投げる
          }
      }
      catch( int e )
      {
          // 再び投げられた例外をとらえる
      }
  
  }


例外がとらえられていない状態でオペランドのないthrow式を実行すると、std::terminateが呼ばれる。



.. code-block:: c++
  
  int main()
  {
      throw ; // std::terminateが呼ばれる
  }


コンストラクターとデストラクター(Constructors and destructors)
--------------------------------------------------------------------------------



処理がthrow式からハンドラーに移るにあたって、tryブロックの中で構築された自動オブジェクトのデストラクターが呼び出される。自動オブジェクトの破棄は構築の逆順に行われる。



.. code-block:: c++
  
  struct X
  {
      X() { }
      ~X() { }
  } ;
  
  
  int main()
  {
      try
      {
          X a ;
          X b ;
          X c ;
          // a, b, cの順に構築される
  
          throw 0 ;
      }
      // このハンドラーに処理が移る過程で、
      // c, b, aの順に破棄される
      catch( int ) { }
  }


オブジェクトの構築、破棄が、例外により中断された場合、完全に構築されたサブオブジェクトに対してデストラクターが実行される。オブジェクトが構築されたストレージの種類は問わない。



.. code-block:: c++
  
  struct Base
  {
      Base() { }
      ~Base() { }
  } ;
  
  
  // コンストラクターに実引数trueが渡された場合、例外を投げるクラス
  struct Member
  {
      Member( bool b )
      {
          if ( b )
              throw 0 ;
      }
      ~Member() { }
  } ;
  
  // Xのサブオブジェクトは、基本クラスBaseと、非staticデータメンバー、a, b, c
  struct X : Base
  {
      Member a, b, c ;
  
      X() : a(false), b(true), c(false)
      { }
      // Base, aのデストラクターが実行される。
      ~X() { }
      
  } ;
  
  
  
  int main()
  {
      try
      {
          X x ;
      }
      catch( int ) { }
  }


この例では、クラスXは、サブオブジェクトとして、Base型の基本クラスと、Member型の非staticデータメンバー、a, b, cを持つ。その初期化順序は、基本クラスBase, a, b, c, Xである。クラスMemberは、コンストラクターの実引数にtrueが渡された場合、例外を投げる。クラスXのコンストラクターは、bのコンストラクターにtrueを与えている。その結果、クラスXのオブジェクトの構築は、例外によって中断される。



この時、デストラクターが実行されるのは、基本クラスBaseのオブジェクトと、Member型の非staticデータメンバーaのオブジェクトである。bは、コンストラクターを例外によって抜けだしたため、構築が完了していない。cは、まだコンストラクターが実行されていないため、構築が完了していない。そのため、b, cのオブジェクトに対してデストラクターは実行されない。



ただし、union風クラスのvariantメンバーには、デストラクターは呼び出されない。



.. code-block:: c++
  
  struct Member 
  {
      Member() { }
      ~Member() { }
  } ;
  
  
  struct X
  {
      union { Member m ; }  ;
  
      X() { throw 0 ; } // mのデストラクターは実行されない
      ~X() { } 
  } ;


あるオブジェクトの非デリゲートコンストラクターの実行が完了し、その非デリゲートコンストラクターを呼び出したデリゲートコンストラクターが例外によって抜けだした場合、そのオブジェクトに対してデストラクターが呼ばれる。



.. code-block:: c++
  
  struct X
  {
      // 非デリゲートコンストラクター
      X( bool ) { }
  
      // デリゲートコンストラクター
      X() : X( true )
      {
          throw 0 ; // Xのデストラクターが呼ばれる
      }
  
      ~X() { }
  } ;


これは、オブジェクトの構築完了は、非デリゲートコンストラクターの実行が完了した時点だからだ。



例外によって構築が中断されたオブジェクトがnew式によって構築された場合、使われた確保関数に対応する解放関数があれば、ストレージを開放するために自動的に呼ばれる。



.. code-block:: c++
  
  struct X
  {
      X() { throw 0 ; }
      ~X() { } 
  
      // 確保関数
      void * operator new( std::size_t size ) noexcept
      {
          return std::malloc( size ) ;
      }
  
      // 上記確保関数に対応する解放関数
      void operator delete( void * ptr ) noexcept
      {
          std::free( ptr ) ;
      }
  } ;
  
  int main()
  {
      try
      {
          new X ; // 対応する解放関数が呼ばれる
      }
      catch( int ) { }
  }


この例では、Xを構築するためにmallocで確保されたストレージは、正しくfreeで解放される。



throw式から処理を移すハンドラーまでのtryブロック内の自動ストレージ上のオブジェクトのデストラクターを自動的に呼ぶこの一連の過程は、スタックアンワインディング(stack unwinding)と呼ばれている。もし、スタックアンワインディング中に呼ばれたデストラクターが例外によって抜けだした場合、std::terminateが呼ばれる。



.. code-block:: c++
  
  struct X
  {
      X() { }
      ~X() noexcept(false)
      {
          throw 0 ;
      }
  } ;
  
  int main()
  {
      try
      {
          X x ;
          throw 0 ; // std::terminateが呼ばれる
      }
      catch( int ) { }
  }


現行の文面を解釈すると、以下のコードもstd::terminateを呼ぶように解釈できるが、これは誤りであり、将来の規格改定で修正されるはずである。



.. code-block:: c++
  
  struct Y
  {
      Y() { }
      ~Y() noexcept(false) { throw 0 ; }
  } ;
  
  struct X
  {
      X() { }
      ~X() noexcept(false)
      {
          try {
          // スタックアンワインディング中に呼ばれたデストラクターが例外によって抜け出す
          // 現行の規格の文面解釈ではstd::terminateが呼ばれてしまう
              Y y ; 
          } catch( int ) { }
      }
  } ;
  
  int main()
  {
      try
      {
          X x ;
          throw 0 ;
      }
      catch( int ) { }
  }


一般に、デストラクターを例外によって抜け出すようなコードは書くべきではない。デストラクターはスタックアンワインディングのために呼ばれるかもしれないからだ。スタックアンワインディング中かどうかを調べる、std::uncaught_exceptionのような標準ライブラリもあるにはあるが、スタックアンワインディング中かどうかを調べる必要は、通常はない。



C++11からは、デストラクターはデフォルトで例外指定がつくようになり、ほとんどの場合、noexcept(true)と互換性のある例外指定になる変更がなされたのも、通常はデストラクターを例外で抜け出す必要がないし、またそうすべきではないからだ。



例外の捕捉(Handling an exception)
--------------------------------------------------------------------------------



throw式によって投げられた例外は、tryブロックのハンドラーによって補足される。ハンドラーの文法は以下の通り。



.. code-block:: c++
  
  catch ( 例外宣言 ) 複合文


.. code-block:: c++
  
  int main()
  {
      try
      {
          throw 0 ; 例外オブジェクトの型はint
      }
      catch( double d ) {} 
      catch( float f ) { }
      catch( int i ) {} // このハンドラーに処理が移る
  
  }


例外が投げられると、処理は、例外オブジェクトの型と適合(match)する例外宣言を持つハンドラーに移される。



ハンドラーの例外宣言は、不完全型、抽象クラス型、rvalueリファレンス型であってはならない。



.. code-block:: c++
  
  struct incomplete ; // 不完全型
  
  struct abstract
  {
      void f() = 0 ;
  } ;
  
  int main()
  {
      try { }
      catch ( incomplete x ) { } // エラー、不完全型
      catch ( abstract a ) { } // エラー、抽象クラス型
      catch( abstract * a ) { } // OK、抽象クラスへのポインター型
      catch( abstract & a ) { } // OK、抽象クラスへのリファレンス型
      catch( int && rref) { } // エラー、rvalueリファレンス型
  }


また、例外宣言の型は、不完全型へのポインターやリファレンスであってはならない。ただし、void *, const void *, volatile void *, const volatile void *は、不完全型へのポインター型だが、例外的に許可されている。




ハンドラーの例外宣言が「Tへの配列」の場合、「Tへのポインター」型に変換される。「Tを返す関数」型は、「Tを返す関数へのポインター」型に変換される。



.. code-block:: c++
  
  catch ( int [5] ) // int *と同じ
  catch ( int f( void ) ) // int (*f)(void)と同じ


あるハンドラーが、例外オブジェクトの型Eと適合する条件は以下の通り



* 
  
ハンドラーの型が cv Tもしくは cv T &amp;で、EとTが同じ型である場合。



  
cvは任意のCV修飾子(const, volatile)のことで、トップレベルのCV修飾子は無視される。



  
たとえば、例外オブジェクトの型がintの場合、以下のようなハンドラーが適合する。



  .. code-block:: c++  
    
    catch ( int )
    catch ( const int )
    catch ( volatile int )
    catch ( const volatile int )
    catch ( int & )
    catch ( const int & )
    catch ( volatile int & )
    catch ( const volatile int & )
  


* 
  
ハンドラーの型がcv Tかcv T &amp;で、TはEの曖昧性のないpublicな基本クラスである場合



  
例えば、以下のような例が適合する。



  .. code-block:: c++  
    
    struct Base { } ;
    struct Derived : public Base { } ;
    
    int main()
    {
        try
        {
            Derived d ;
            throw d ; // 例外オブジェクトの型はDerived
        }
        catch( Base & ) { } // 適合、BaseはDerivedの曖昧性のないpublicな基本クラス
    }
  

  
以下のような例は適合しない。



  .. code-block:: c++  
    
    struct Base { } ;
    struct Ambiguous { } ;
    struct Derived : private Base, public Ambiguous { } ;
    
    struct Sub : public Derived, public Ambiguous { } ;
    
    int main()
    {
        try
        {
            Sub sub ;
            throw sub ; // 例外オブジェクトの型はSub
        }
        catch( Base & ) { } // 適合しない、非public基本クラス
        catch( Ambiguous & ) { } // 適合しない、曖昧
    }
  


* 
  
ハンドラーの型がcv1 T* cv2で、Eがポインター型で、以下のいずれかの方法でハンドラーの型に変換可能な場合



  *   
  
標準ポインター型変換で、privateやprotectedなポインターへの変換や、曖昧なクラスへの変換を伴わないもの



  .. code-block:: c++  
    
    struct Base { } ;
    struct Derived : public Base { } ;
    
    int main()
    {
        try
        {
            Derived d ;
            throw &d ; // 例外オブジェクトの型はDerived
        }
        catch( Base * ) { } // 適合、BaseはDerivedの曖昧性のないpublicな基本クラス
    }
  


  *   
  
修飾変換



  .. code-block:: c++  
    
    int main()
    {
        int i ;
        try
        {
    
            throw &i ;
        }
        catch( const int * ) { }
    }
  





* 
  
ハンドラーの型がポインターかメンバーへのポインターで、Eがstd::nullptr_tの場合



  .. code-block:: c++  
    
    struct X
    {
        int member ;
    } ;
    
    int main()
    {
        try
        {
            throw nullptr ;
        }
        catch( void * ) { } // 適合
        catch( int * ) { } // 適合
        catch( X * ) { } // 適合
        catch( int X::* ) { } // 適合
    }
  

  
nullptrの型であるstd::nullptr_t型の例外オブジェクトは、あらゆるポインター型、メンバーへのポインター型に適合する。






throw式のオペランドが定数式で0と評価される場合でも、ポインターやメンバーへのポインター型のハンドラーには適合しない。



.. code-block:: c++
  
  int main()
  {
      try
      {
          throw 0 ; // 例外オブジェクトの型はint
      }
      catch( int * ) // 適合しない
  }


tryブロックのハンドラーは、書かれている順番に比較される。



.. code-block:: c++
  
  int main()
  {
      try
      {
          throw 0 ; // 例外オブジェクトの型はint
      }
      catch ( int ) { } // 適合する。処理はこのハンドラーに移る
      catch ( const int ) { }
      catch ( int & ) { }
  }


この例では、3つのハンドラーはどれも例外オブジェクトの型に適合するが、比較は書かれている順番に行われる。一番初めに適合したハンドラーに処理が移る。関数のオーバーロード解決のような、ハンドラー同士の型の適合の優劣の比較は行われない。



ハンドラーの例外宣言に...が使われた場合、そのハンドラーはどの例外にも適合する。



.. code-block:: c++
  
  void f()
  {
      try { }
      catch( int ) { }
      catch( double ) { }
      catch( ... ) { } // どの例外にも適合する
  }


...ハンドラーを使う場合は、tryブロックのハンドラーの最後に記述しなければならない。



.. code-block:: c++
  
  void f()
  {
      try { }
      catch( ... ) { }
      catch( int ) { } // エラー
  }


tryブロックのハンドラーのうちに、適合するハンドラーが見つからない場合、同じスレッド内で、そのtryブロックのひとつ上のtryブロックが試みられる。



.. code-block:: c++
  
  void f()
  {
      try { throw 0 ; } // 例外オブジェクトの型はint
      catch( double ) { } // 適合しない
  }
  
  void g()
  {
  
      try
      {
          f() ;
      }
      catch( int ) { } // 適合する
  }
  
  int main()
  {
      try {
          g() ;
      }
      catch( ... ) { }
  }


catch句の仮引数の初期化が完了した時点で、ハンドラーはアクティブ(active)になったとみなされる。スタックはこの時点でアンワインドされている。例外を投げた結果、std::terminateやstd::unexpectedが呼ばれた場合、暗黙のハンドラーというものがアクティブになったものとみなされる。catch句から抜けだした場合、ハンドラーはアクティブではなくなる。



現在、アクティブなハンドラーが存在する場合、直前に投げられた例外を、現在補足されている例外(currently handled exception)と呼ぶ。



適合するハンドラーが見つからない場合、std::terminateが呼ばれる。std::terminateが呼ばれる際、スタックがアンワインドされるかどうかは実装次第である。



コンストラクターとデストラクターの関数tryブロック内で、非staticデータメンバーかオブジェクトの基本クラスを参照した場合、挙動は未定義である。



.. code-block:: c++
  
  struct S
  {
      int member ;
  
      S()
      try
      {
          throw 0 ;
      }
      catch ( ... )
      {
          int x = member ; // 挙動は未定義
      }
  } ;


コンストラクターの関数tryブロックのハンドラーに処理が移る前に、完全に構築された基本クラスと非staticメンバーのオブジェクトは、破棄される。



.. code-block:: c++
  
  struct Base
  {
      Base() { }
      ~Base() { }
  } ;
  
  struct Derived : Base
  {
  
      Derived()
      try
      {
          throw 0 ;
      }
      catch ( ... )
      {
          // 基本クラスBaseのオブジェクトはすでに破棄されている
          // 非staticデータメンバーのオブジェクトについても同様
      }
  } ;


オブジェクトの非デリゲートコンストラクターの実行が完了したあとに、デリゲートコンストラクターが例外を投げた場合は、オブジェクトのデストラクターが実行されたあとに、関数tryブロックのハンドラーに処理が移る。



.. code-block:: c++
  
  struct S
  {
  
      // 非デリゲートコンストラクター
      S() { }
  
      // デリゲートコンストラクター
      S( int ) try
          : S()
      { throw 0 ; }
      catch( ... )
      {
          // デストラクターS::~Sはすでに実行されている
      }
  
      ~S() { }
  } ;
  
  int main()
  {
      S s(0) ;
  }


非デリゲートコンストラクターの実行完了をもって、オブジェクトは構築されている。デリゲートコンストラクターが例外を投げた場合の関数tryブロックのハンドラーに処理が移る前に、オブジェクトを破棄されなければならない。そのために、ハンドラーに処理が移る前にデストラクターが呼び出されることになる。



デストラクターの関数tryブロックのハンドラーに処理が移る前に、オブジェクトの基本クラスと非variantメンバーは破棄される。



.. code-block:: c++
  
  struct Base
  {
      Base() { }
      ~Base() { }
  } ;
  
  struct Derived : Base
  {
      ~Derived() noexcept(false)
      try { throw 0 ; }
      catch( ... )
      {
          // 基本クラスはすでに破棄されている
          // 非staticデータメンバーについても同様
      }
  } ;


関数のコンストラクターの仮引数のスコープと寿命は、関数tryブロックのハンドラー内まで延長される。



.. code-block:: c++
  
  void f( int param )
  try
  {
      throw 0 ;
  }
  catch ( ... )
  {
      int x = param ; // OK、延長される
  }


静的ストレージ上のオブジェクトのデストラクターから投げられる例外が、main関数の関数tryブロックのハンドラーで補足されることはない。threadストレージ上のオブジェクトのデストラクターから投げられる例外が、スレッドの初期関数の関数tryブロックのハンドラーで補足されることはない。



コンストラクターの関数tryブロックのハンドラーの中にreturn文がある場合、エラーとなる。



.. code-block:: c++
  
  struct S
  {
      S()
      try { }
      catch( ... )
      {
          return ; // エラー
      }
  } ;


コンストラクターとデストラクターの関数tryブロックで、処理がハンドラーの終わりに達したときは、現在ハンドルされている例外が、再びthrowされる。



.. code-block:: c++
  
  struct S
  {
      S()
      try {
          throw 0 ;
      }
      catch ( int )
      {
          // 例外が再びthrowされる
      }
  } ;


コンストラクターとデストラクター以外の関数の関数tryブロック、処理がハンドラーの終わりに達したときは、関数からreturnする。このreturnは、オペランドなしのreturn文と同等になる。



.. code-block:: c++
  
  void f()
  try
  {
      throw 0 ;
  }
  catch( int )
  {
  // return ;と同等
  }


もしこの場合に、関数が戻り値を返す関数の場合、挙動は未定義である。



int f()
try
{
    throw 0 ;
}
catch( ... )
{
// 挙動は未定義
}



例外宣言が例外の型と名前を指定する場合、例外の型のオブジェクトがその名前で、例外オブジェクトからコピー初期化される。



.. code-block:: c++
  
  int main()
  {
      try
      {
          throw 123 ; // 例外オブジェクの型はint、値は123
      }
      catch( int e )
      {
          // eの型はint、値は123
      }
  }


例外宣言が、例外の型のみで名前を指定していない場合、例外の型の一時オブジェクトが生成され、例外オブジェクトからコピー初期化される



.. code-block:: c++
  
  int main()
  {
      try
      {
          throw 123 ;
      }
      catch( int )
      {
          // int型の一時オブジェクトが生成され、例外オブジェクトからコピー初期化される
          // 名前がないので、参照する方法はない
      }
  }


例外宣言の名前の指し示すオブジェクト、あるいは無名の一時オブジェクトの寿命は、処理がハンドラーから抜けだして、ハンドラー内で初期化された一時オブジェクトが解放された後である。



.. code-block:: c++
  
  struct S
  {
      int * p ;
      S( int * p ) : p(p) { }
      ~S() { *p = 0 ; }
  } ;
  
  int main()
  {
      try
      {
          throw 123 ;
      }
      catch( int e )
      {
          S s( &e ) ;
      
      // sが破棄された後に、eが破棄される
      }
  }


そのため、上のコードは問題なく動作する。なぜならば、eが破棄されるのはsよりも後だからだ。



ハンドラーの例外宣言が、非constな型のオブジェクトの場合、ハンドラー内でそのオブジェクトに対する変更は、throw式によって生成された一時的な例外オブジェクトには影響しない。



.. code-block:: c++
  
  int main()
  {
      try
      {
          try
          {
              throw 0 ;
          }
          catch( int e )
          {
              ++e ; // 変更
              throw ; // 例外オブジェクトの再throw
          }
      }
      catch ( int e )
      {
          // eは0
      }
  }


ハンドラーの例外宣言が、非constな型へのリファレンス型のオブジェクトの場合、ハンドラー内でそのオブジェクトに対する変更は、throw式によって生成された一時的な例外オブジェクトを変更する。この副作用は、ハンドラー内で再throwされたときにも効果を持つ。



.. code-block:: c++
  
  int main()
  {
      try
      {
          try
          {
              throw 0 ;
          }
          catch( int & e )
          {
              ++e ; // 変更
              throw ; // 例外オブジェクトの再throw
          }
      }
      catch ( int e )
      {
          // eは1
      }
  }


例外指定(Exception specifications)
--------------------------------------------------------------------------------



例外指定(Exception specification)とは、関数宣言で、関数が例外を投げるかどうかを指定する機能である。



関数宣言における例外指定の文法は、リファレンス修飾子の後、アトリビュートの前に記述する。



.. code-block:: c++
  
  T D( 仮引数宣言 ) cv修飾子 リファレンス修飾子 例外指定 アトリビュート指定子
  
  例外指定:
  noexcept( 定数式 )
  noexcept


.. code-block:: c++
  
  void f() noexcept ;
  
  struct S
  {
      void f() const & noexcept [[ ]] ;
  } ;


例外指定は、関数宣言と定義のうち、関数型、関数へのポインター型、関数型へのリファレンス、メンバー関数へのポインター型に適用できる。また、関数へのポインター型が仮引数や戻り値の型に使われる場合も指定できる。



.. code-block:: c++
  
  void f() noexcept           ; // OK
  void (*fp)() noexcept = &f  ; // OK
  void (&fr)() noexcept = f   ; // OK
  
  // OK、仮引数として
  void g( void (*fp)() noexcept ) ;
  // OK、戻り値の型として
  auto h() -> void (*)() noexcept ;
  
  struct S
  {
      void f() noexcept ; // OK
  } ;


typedef宣言とエイリアス宣言には使用できない。



.. code-block:: c++
  
  typedef void (*func_ptr_type)() noexcept ; // エラー
  using type = void (*)() noexcept ; // エラー


例外指定のない関数宣言は、例外を許可する関数である。



例外指定にnoexceptが指定された場合、その関数は例外を許可しないと指定したことになる。




例外指定に、noexcept(定数式)を指定し、定数式がtrueと評価される場合、その関数は例外を許可しないと指定したことになる。定数式がfalseと評価される場合、その関数は例外を許可する関数と指定したことになる。



.. code-block:: c++
  
  void f1() ; // 例外を許可
  void f2() noexcept ; // 例外を許可しない
  void f3() noexcept( true ) ; // 例外を許可しない
  void f4() noexcept( false ) ; // 例外を許可


noexcept(定数式)は、コンパイル時の条件に従って、関数の例外指定を変えることに使える。



.. code-block:: c++
  
  template < typename T >
  constexpr bool is_nothrow()
  {
      return std::is_fundamental<T>::value ;
  }
  
  // テンプレート仮引数が基本型なら例外を投げない実装ができる関数
  template < typename T >
  void f( T x ) noexcept( is_nothrow<T>() ) ;


この例では、関数fは、テンプレート仮引数が基本型の場合、例外を投げない実装ができるものとする。そこで、テンプレートのインスタンス化の際に、型を調べることによって、例外を許可するかどうかをコンパイル時に切り替えることができる。



もし、例外を許可しない関数が、例外のthrowによって抜け出した場合、std::terminateが呼ばれる。



.. code-block:: c++
  
  // 例外を許可する関数
  void allow_exception()
  {
      throw 0 ; // OK
  }
  
  // 例外を許可しない関数
  void disallow_exception() noexcept
  {
      try
      {
          throw 0 ; // OK、例外は関数の外に抜けない
      }
      catch ( int ) { }
  
      throw 0 ; // 実行時にstd::terminateが呼ばれる
  }


例外を許可しないというのは、例外によって関数から抜け出すことを禁止するものであり、関数の中で例外を使うことを禁止するものではない。



例外を許可しない関数は、例外を投げる可能性があったとしても、違法ではない。C++実装は、そのようなコードを合法にするように明確に義務付けられている。



.. code-block:: c++
  
  void f() noexcept
  {
      throw 0 ; // OK、コンパイルが通る
      // 実行時にstd::terminateが呼ばれる
  }
  
  void g( bool b ) noexcept
  {
      if ( b )
          throw 0 ; // OK、コンパイルが通る
      // 実行時にbがtrueの場合、std::terminateが呼ばれる
  }


もちろん、そのような関数を呼び出して、結果として関数の外に例外が投げられた場合、std::terminateが呼ばれる。



この他に、C++11では非推奨(deprecated)扱いになっている機能に、動的例外指定(dynamic-exception-specification)がある。この機能は将来廃止されるので、詳しく解説しないが、概ね以下のような機能となっている。



.. code-block:: c++
  
  // 例外を許可しない
  void f() throw( ) ; 
  
  // int型のthrowを許可する
  void g() throw( int ) ;
  
  // int型とshort型のthrowを許可する
  void h() throw( int, short ) ;


動的例外指定のある関数では、例外を関数の外にthrowすると、std::unexpectedが呼ばれる。もし、許可した型の例外をthrowした場合は、そのままハンドラーの検索が行われるが、許可しない型をthrowした場合は、std::terminateが呼ばれるとされている。



少なくとも、当初のC++の設計はそうであったが、現実には、そのように実装するC++実装は出てこなかった。ほとんどの実装では、動的例外指定は、単に無視された。



その後、何も例外として許可する型を指定子ない、throw()だけが、関数が例外を外に投げないものとして



クラスの暗黙に宣言される特別なメンバー関数は、この動的例外指定を暗黙に指定される。その型リストは、暗黙の実装が呼び出す関数が投げる可能性のある例外のみを持つ。



これは、基本クラスや非staticメンバーが、明示的に例外を許可するものでないかぎり、クラスの暗黙の特別なメンバーは、無例外指定されるということである。



.. code-block:: c++
  
  class S
  {
  // 暗黙のコンストラクター、デストラクター、代入演算子は、
  // 例外指定throw()が指定される
  } ;


解放関数の宣言に、明示的な例外指定がない場合は、noexcept(true)が指定されたものとみなされる。



.. code-block:: c++
  
  // 暗黙にnoexcept(true)が指定される
  void operator delete( void * ) ;


