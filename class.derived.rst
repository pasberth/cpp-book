派生クラス（Derived classes）
================================================================================

複数の基本クラス（Multiple base classes）
--------------------------------------------------------------------------------



基本クラスは、複数指定することができる。これを、複数の基本クラスという。複数の基本クラスを指定することを、俗に、多重継承（Multiple Inheritance）ということがあるが、これは、C++の規格上、正しい用語ではない。継承は、基本クラスのメンバーを派生クラスも受け継ぐことを意味する用語であって、クラスの派生関係を表すのに使う言葉ではないからだ。



ただし、歴史的に言えば、Multiple Inheritanceという言葉を最初に使ったのは、他ならぬBjarne Stroustrupご本人である。当時、Stroustrup氏が複数の基本クラスの設計をしていた時に使った言葉が、多重継承であった。ちなみに、多重継承が初めて使われたコードは、Jerry Schwarzによって書かれたiostreamである。



複数の基本クラスは、コンマで区切ることによって指定する。



.. code-block:: c++
  
  struct A { } ; struct B { } ; struct C { } ;
  struct D
       : A, B, C
  { } ;


この例では、Dは、A、B、Cという3個の基本クラスを持っている。



同じクラスを複数、直接の基本クラスとして指定することは出来ない。間接の基本クラスとしては指定できる。



.. code-block:: c++
  
  struct Base { } ;
  
  struct Derived
       : Base, Base // エラー、直接の基本クラス
  { } ;
  
  struct Derived1 : Base { } ;
  struct Derived2 : Base { } ;
  struct Derived3
       : Derived1, Derived2 // OK、間接の基本クラス
      { } ;


この場合、Derived3は、Baseクラスのサブオブジェクトを、2個持つことになる。



基本クラスに、virtualが指定されていない場合、非virtual基本クラス（non-virtual base class）となる。非virtual基本クラスには、それぞれ独立したサブオブジェクトが割り当てられる。



<p class="editorial-note">
TODO: 派生階層を表現する図



同じクラスが複数、非virtual基本クラスとして存在することは、基本クラスのメンバーの名前に対するオブジェクトが容易に曖昧になる。このとき、派生クラスから基本クラスのメンバーを使うには、名前を正しく修飾しなければならない。



.. code-block:: c++
  
  struct Base { int member ; } ;
  struct Derived1 : Base { } ;
  struct Derived2 : Base { } ;
  
  // Derived3には、2個のBaseサブオブジェクトが存在する
  struct Derived3 : Derived1, Derived2
  {
      void f()
      {
          member ; // エラー、曖昧
          Base::member ; // エラー、曖昧
          Derived1::member ; // OK
          Derived2::member ; // OK
      }
  } ;
  
  int main()
  {
      Derived3 x ;
      x.member ; // エラー、曖昧
      x.Derived1::member ; // OK
      x.Derived2::member ; // OK
  }


ただし、staticメンバーの名前は、曖昧にならない。これは、staticメンバーの利用には、クラスのオブジェクトは必要ないからである。



.. code-block:: c++
  
  struct Base
  {
      static void static_member() { }
      static int static_data_member ;
  } ;
  int Base::static_data_member = 0 ;
  
  struct Derived1 : Base { } ;
  struct Derived2 : Base { } ;
  
  struct Derived3 : Derived1, Derived2
  {
      void f()
      {
          static_member() ; // OK
          static_data_member ; // OK
      }
  } ;


直接、間接の両方の基本クラスに、同じクラスを持つことは可能である。ただし、そのような派生クラスは、基本クラスの非staticメンバーを使うことができない。なぜなら、基本クラスの名前自体の曖昧性を解決する方法がないからだ。



.. code-block:: c++
  
  struct Base
  {
      int member() ; // 非staticメンバー
      static void static_member() { } // staticメンバー
  } ;
  struct Derived1 : Base { } ;
  
  // Baseという名前自体が曖昧になる
  struct Derived2 : Base, Derived1
  {
      void f()
      {
          // Baseの非staticメンバーを使う方法はない
  
          static_member() ; // OK、staticメンバーは使える
      }
  } ;


このため、直接、間接の両方で同じクラスを基本クラスに持つ派生クラスの利用は、かなり制限される。



基本クラスに、virtualが指定されている場合、virtual基本クラス（virtual base class）という。virtual基本クラスには、ひとつしかオブジェクトが割り当てられない。virtual基本クラスのオブジェクトは、派生クラスで共有される。



.. code-block:: c++
  
  struct L { } ;
  struct A : virtual L { } ;
  struct B : virtual L { } ;
  struct C : A, B { } ;


<p class="editorial-note">
TODO: クラス階層を表す図



この例で、Cクラスには、Lのサブオブジェクトは1個存在する。これは、A、Bで共有される。



virtual基本クラスでは、サブオブジェクトが共有されているため、virtual基本クラスのメンバーは、曖昧にならない。



.. code-block:: c++
  
  struct Base { int member ; } ;
  struct Derived1 : virtual Base { } ;
  struct Derived2 : virtual Base { } ;
  struct Derived3 : Derived1, Derived2
  {
      void f()
      {
          member ; // OK
      }
  } ;


非virtual基本クラスとvirtual基本クラスは、両方持つことができる。



.. code-block:: c++
  
  struct B { } ;
  struct X : virtual B { } ;
  struct Y : virtual B { } ;
  struct Z : B { } ;
  struct A : X, Y, Z { } ;


<p class="editorial-note">
TODO:クラス階層を表す図



この例では、Aクラスには、Bのサブオブジェクトは、2個存在する。X、Yで共有されるサブオブジェクトと、Zのサブオブジェクトである。


メンバーの名前探索（Member name lookup）
--------------------------------------------------------------------------------



メンバーの名前探索は、すこし難しい。派生クラスのメンバー名は、基本クラスのメンバー名を隠すということだ。あるメンバー名を名前探索する際に、派生クラスで名前が見つかった場合、その時点で名前探索は終了する。基本クラスのメンバーを探すことはない。



.. code-block:: c++
  
  struct Base
  {
      void f( int ) { }
  } ;
  
  struct Derived : Base
  {
      void f( double ) { }
  } ;
  
  int main()
  {
      Derived object;
      object.f( 0 ) ; // Derived::f( double )が呼ばれる
  }


ここで、Derivedクラスには、二つのfという名前のメンバーが存在する。Derived::fとBase::fである。もし、名前探索によって両方の名前が発見された場合、オーバーロード解決によって、Base::f(int)が選ばれるはずである。しかし、実際には、Derived::f(double)が選ばれる。これは、Derivedクラスに、fという名前のメンバーが存在するので、その時点で名前探索が終了するからである。Baseのメンバー名は発見されない。名前が発見されない以上、オーバーロード解決によって選ばれることもない。



これは、名前探索に対するルールなので、型は関係がない。



.. code-block:: c++
  
  // fという名前のint型のデータメンバー
  struct Base { int f ; } ;
  // fという名前のvoid (void)型のメンバー関数
  struct Derived : Base { void f( ) { } } ;
  
  int main()
  {
      Derived object;
      object.f = 0 ; // エラー、メンバー関数Derived::fに0を代入することはできない
      object.Base::f = 0 ; // OK、明示的な修飾
  }


したがって、基本クラスと同じ名前のメンバーを派生クラスで使う際には、注意が必要である。



名前探索という仕組みを考えずに、この挙動を考えた場合、これは、派生クラスのメンバー名が、基本クラスのメンバー名を、隠していると考えることもできる。もし、基本クラスのメンバー名を隠したくない場合、<a href="#namespace.udecl">using宣言</a>を使うことができる。using宣言を使うと、基本クラスのメンバー名を、派生クラスのスコープに導入することができる。



.. code-block:: c++
  
  struct Base
  {
      void f( int ) { }
  } ;
  
  struct Derived : Base
  {
      using Base::f ; // using宣言
      void f( double ) { }
  } ;
  
  int main()
  {
      Derived object;
      object.f( 0 ) ; // Base::f( int )が呼ばれる
  }


名前探索で、派生クラスのメンバーが見つからない場合は、直接の基本クラスのメンバーから、名前が探される。



.. code-block:: c++
  
  struct Base { int member ; } ;
  struct Derived : Base
  {
      void f()
      {
          member ; // Base::member
      }
  } ;


メンバー名を探す基本クラスは、直接の基本クラスだけである。間接の基本クラスのメンバーは、直接の基本クラスを通じて、探される。



.. code-block:: c++
  
  struct A { int member ; } ;
  struct B : A { } ;
  struct C : B
  {
      void f()
      {
          member ; // A::member
      } 
  } ;


この例では、C::fでmemberという名前のメンバーを使っている。Cクラスにはmemberという名前のメンバーが見つからないので、名前探索はBクラスに移る。クラスは、基本クラスのメンバー名を継承している。そのため、Bクラスの基本クラスのAクラスのメンバー名は、Bクラスのスコープからも発見することができる。



直接の基本クラスが複数ある場合、それぞれの直接の基本クラスから、名前が探される。この際、複数のクラスから同じ名前が発見され、名前の意味が違う場合、名前探索は無効となる。



.. code-block:: c++
  
  struct Base1 { void member( int ) { } } ;
  struct Base2 { void member( double ) { } } ;
  struct Derived : Base1, Base2 // 複数の直接の基本クラス
  {
      void f()
      {
          member( 0 ) ; // エラー、名前探索が無効
          Base1::member( 0 ) ; // OK
      } 
  } ;


これは、memberという名前に対し、複数の直接の基本クラスで、複数の同じ名前が見つかり、しかも意味が違っているので、名前検索が無効となる。その結果、memberという名前が見つからず、エラーとなる。



もし、この例で、Derivedから、明示的な修飾をせずに、両方の基本クラスのメンバー関数を呼び出したい場合、<a href="#namespace.udecl">using宣言</a>が使える。



.. code-block:: c++
  
  struct Base1 { void member( int ) { } } ;
  struct Base2 { void member( double ) { } } ;
  struct Derived : Base1, Base2
  {
      // 基本クラスのメンバー名をDerivedスコープで宣言する
      using Base1::member ;
      using Base2::member ;
  
      void f()
      {
          member( 0 ) ; // OK、オーバーロード解決により、Base1::member(int)が呼ばれる
      } 
  } ;


この例は、複数の直接の基本クラスがある場合の制限である。複数の間接の基本クラスでは、名前探索が失敗することはない。ただし、名前探索の結果として、複数の名前が発見され、曖昧になることはある。


virtual関数（Virtual functions）
--------------------------------------------------------------------------------



本書のサンプルコードは、解説する文法のための最小限のコードであり、virtual関数を持つクラスがvirtualデストラクターを持たないことがある。これは現実ではほとんどの場合、不適切である。



メンバー関数にvirtual指定子を指定すると、virtual関数となる。virtual関数を宣言しているクラス、あるいはvirtual関数を継承しているクラスは、ポリモーフィッククラス（polymorphic class）となる。



.. code-block:: c++
  
  struct Base
  {
      virtual void f() { } // virtual関数
  } ;
  struct Derived : Base { } ;


BaseとDerivedは、ポリモーフィッククラスである。



クラスがポリモーフィックであるかどうかということは、dynamic_castやtypeidを使う際に、重要である。



基本クラスのvirtual関数は、派生クラスのメンバーに、同じ名前、同じ仮引数リスト、同じCV修飾子、同じリファレンス修飾子という条件を満たすメンバー関数があった場合、オーバーライドされる。この時、派生クラスのメンバー関数は、virtual指定子がなくても、自動的にvirtual関数になる。



.. code-block:: c++
  
  struct A { virtual void f() {} } ;
  struct B : A { } ; // オーバーライドしない
  struct C : A
  {
      void f() { } // オーバーライド
  } ;
  struct D : C
  {
      void f(int) { } // オーバーライドしない
      void f() const { } // オーバーライドしない
  } ;
  
  // リファレンス修飾子が違う例
  struct Base { virtual void f() & { } } ;
  struct Derived : Base { void f() && { } } ;


もちろん、virtualをつけてもよい。



.. code-block:: c++
  
  struct Base { virtual f() { } } ;
  struct Derived : Bae { virtual f() { } }  ; // オーバーライド


派生クラスで、最後にオーバーライドしたvirtual関数を、ファイナルオーバーライダー（final overrider）と呼ぶ。あるクラスのオブジェクトに対して、virtual関数を呼び出す際は、オブジェクトの実行時の型によって、最後にオーバーライドしたvirtual関数が呼び出される。これは、基本クラスのポインターやリファレンスを経由してオブジェクトを使った場合でも、同様である。通常のメンバー関数は、virtual関数とは違い、実行時の型チェックを行わない。オブジェクトを指しているリファレンスやポインターの型によって、決定される。



.. code-block:: c++
  
  // virtual関数と非virtual関数の違いの例
  struct A
  {
      virtual void virtual_function() { }
      void function() { }
  } ;
  struct B : A
  {
      virtual void virtual_function() { }
      void function() { }
  } ;
  struct C : B
  {
      virtual void virtual_function() { }
      void function() { }
  } ;
  
  void call( A & ref )
  {
      ref.virtual_function() ;
      ref.function() ;
  }
  
  int main()
  {
      A a ; B b ; C c ;
  
      call( a ) ; // A::virtual_function, A::functionが呼び出される
      call( b ) ; // B::virtual_function, A::functionが呼び出される
      call( c ) ; // C::virtual_function, A::functionが呼び出される
  }


Aは、virtual_functionとfunctionという名前のvirtual関数を持っており、Aから派生しているB、Bから派生しているCは、オーバーライドしている。call関数の仮引数refは、オブジェクトの型が、実際に何であるかは、実行時にしか分からない。virtual関数であるvirtual_functionは、オブジェクトの型に合わせて正しく呼び出されるが、virtual関数ではないfunctionは、Aのメンバーが呼び出される。



virt指定子(final, override)は、virtual関数の宣言子の後、pure指定子の前に記述できる。



.. code-block:: c++
  
  // virt指定子の文法の例示のための記述
  virtual f() final override = 0 ;


finalが指定されたvirtual関数を持つクラスから派生したクラスが、同virtual関数をオーバーライドした場合はエラーになる。



.. code-block:: c++
  
  struct base
  {
      virtual void f() { }
  } ;
  
  struct derived
  {
      virtual void f() final { }
  } ;
  
  struct ok : derived
  {
  // OK
  } ;
  
  struct error : derived
  {
      // エラー、final指定されているderived::fをオーバーライド
      virtual void f() { }
  } ;


virtual関数にfinalを指定すると、それ以上のオーバーライドを禁止できる。



overrideが指定されたvirtual関数が、基本クラスのメンバー関数をオーバーライドしていない場合、エラーとなる。



.. code-block:: c++
  
  struct base
  {
      virtual void virtual_function() { }
  } ;
  
  struct ok : base
  {
      // OK、ok::virtual_functionはbase::virtual_functionをオーバーライドしている
      virtual void virtual_function() override { }
  } ;
  
  struct typo : base
  {
      // OK、typo::virtal_functionはbase::virtual_functionとは別のvirtual関数
      virtual void virtal_function() { }
  } ;
  
  struct error : base
  {
      // エラー、error::virtal_functionはオーバーライドしていない
      virtual void virtal_function() override { }
  } ;


これにより、タイプミスによる些細な間違いをコンパイル時に検出できる。



オーバーライドであることに注意。以下のコードはエラーである。



.. code-block:: c++
  
  struct base
  {
      void f() { } // 非virtual関数
  } ;
  
  struct error : base
  {
      // エラー、オーバーライドしていない
      virtual void f() override { }
  } ;


finalとoverrideを両方指定することもできる。



virtual関数をオーバーライドする関数は、戻り値の型が同じでなくても構わない。ただし、何でもいいというわけではない。戻り値の型は、まったく同じ型か、相互変換可能（covariant）でなければならない。covariantは、以下のような条件をお互いに満たした型のことである。



今、関数D::fが、関数B::fをオーバーライドしているとする。



.. code-block:: c++
  
  // D::f、B::fの例
  struct B { virtual 戻り値の型 f() ; } ;
  struct D : B { virtual 戻り値の型 f() ; } ;


その場合、戻り値の型は、以下の条件を満たさなければならない。




お互いにクラスへのポインター、もしくは、お互いにクラスへのlvalueリファレンス、もしくは、お互いにクラスへのrvalueリファレンスであること。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

片方がポインターで片方がリファレンスの場合や、片方がlvalueリファレンスで片方がrvalueリファレンスの場合は、不適である。もちろん、ポインターでもリファレンスでもない型は不適である。また、クラスでもない型へのポインターやリファレンスも不適である。



.. code-block:: c++
  
  // ポインター
  struct B { virtual B * f() ; } ;
  struct D : B { virtual D * f() ; } ;
  // lvalueリファレンス
  struct B { virtual B & f() ; } ;
  struct D : B { virtual D & f() ; } ;
  // rvalueリファレンス
  struct B { virtual B && f() ; } ;
  struct D : B { virtual D && f() ; } ;



B::fの戻り値の型のクラスは、D::fの戻り値の型のクラスと同じか、曖昧がなくアクセスできる基本クラスでなければならない。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

オーバーライドしている関数が、基本クラスを戻り値に使っていたり、そもそもクラスの派生関係にない場合は、不適である。private派生していて、派生クラスからはアクセスできない場合や、基本クラスのサブオブジェクトが複数あって曖昧な場合はエラーとなる。



.. code-block:: c++
  
  struct Base { } ; // 基本クラス
  struct Derived : Base { } ; // 派生クラス
  struct Other { } ; // BaseやDerivedとは派生関係にないクラス
  
  // クラスが同じ
  struct B { virtual Base & f() ; } ;
  struct D : B { virtual Base & f() ; } ;
  
  // B::fのクラスはD::fのクラスの基本クラス
  struct B { virtual Base & f() ; } ;
  struct D : B { virtual Derived & f() ; } ;
  
  // エラー
  struct B { virtual Derived & f() ; } ;
  struct D : B { virtual Base & f() ; } ;
  
  // エラー
  struct B { virtual Base & f() ; } ;
  struct D : B { virtual Other & f() ; } ;



両方のポインターは同じCV修飾子を持たなければならない。D::fの戻り値の型のクラスは、B::fの戻り値の型のクラスと同じCV修飾子を持つか、あるいは少ないCV修飾子を持たなければならない。

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

補足：ポインターに対するCV修飾子とは、T cv1 * cv2という型がある場合、cv2である。クラスに対するCV修飾子は、cv1である。



.. code-block:: c++
  
  // int *に対するCV修飾子
  int * const 
  // intに対するCV修飾子
  const int *
  int const *


.. code-block:: c++
  
  // 両方のポインターは同じCV修飾子を持たなければならない例
  
  // ポインターのCV修飾子はconst
  struct B { virtual B * const f() ; } ;
  // OK
  struct D : B { virtual D * const f() ; } ;
  
  // エラーのDクラスの例、ポインターのCV修飾子が一致していない
  struct D : B { virtual D * f() ; } ;
  struct D : B { virtual D * volatile const f() ; } ;
  struct D : B { virtual D * const volatile f() ; } ;


.. code-block:: c++
  
  // D::fの戻り値の型のクラスは、B::fの戻り値の型のクラスと同じCV修飾子を持つか、
  // あるいは少ないCV修飾子を持たなければならない例
  
  // B::fの戻り値の型のクラスのCV修飾子はconst
  struct B { virtual B const & f() ; } ;
  // 問題ないDクラスの例、CV修飾子が同じか少ない
  struct D : B { virtual D const & f() ; } ;
  struct D : B { virtual D & f() ; } ;
  
  // エラーのDクラスの例、CV修飾子が多い
  struct D : B { virtual D volatile & f() ; } ;
  struct D : B { virtual D const volatile & f() ; } ;


明示的な修飾を用いた場合は、virtual関数呼び出しが阻害される。これは、オーバーライドしたvirtual関数から、オーバーライドされたvirtual関数を呼び出すのに使える。



.. code-block:: c++
  
  struct Base { virtual void f() { } } ;
  struct Derived : Base
  {
      virtual void f()
      {
          f() ; // Derived::fの呼び出し
          Base::f() ; // 明示的なBase::fの呼び出し
      }
  } ;


virtual関数とdelete定義は併用できる。ただし、delete定義のvirtual関数を、非delete定義のvirtual関数でオーバーライドすることはできない。非delete定義のvirtual関数を、delete定義のvirtual関数でオーバーライドすることはできない。



.. code-block:: c++
  
  // OK、delete定義のvirtual関数を、delete定義のvirtual関数でオーバーライドしている
  struct Base { virtual void f() = delete ; } ;
  struct Derived : Base { virtual void f() = delete ; } ;
  
  // エラー、非delete定義ではないvirtual関数を、delete定義のvirtual関数でオーバーライドしている
  struct Base { virtual void f() { } } ;
  struct Derived : Base { virtual void f() = delete ; } ;
  
  // エラー、delete定義のvirtual関数を、非delete定義のvirtual関数でオーバーライドしている
  struct Base { virtual void f() = delete ; } ;
  struct Derived : Base { virtual void f() { } } ;


アブストラクトクラス（Abstract classes）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  ピュア指定子:
      = 0 


アブストラクトクラス（abstract class）は、抽象的な概念としてのクラスを実現する機能である。これは、例えば図形を表すクラスである、CircleやSquareなどといったクラスの基本クラスであるShapeや、動物を表すDogやCatなどといったクラスの基本クラスであるAnimalなど、異なるクラスに対する共通のインターフェースを提供する目的に使える。



.. code-block:: c++
  
  struct Shape
  {
      // 図形描画用の関数
      // Shapeクラスは抽象的な概念であり、具体的な描画方法を持たない
      // 単に共通のインターフェースとして提供される
      virtual void draw() = 0 ;
  } ;
  
  struct Circle : Shape
  {
      virtual void draw() { /* 円を描画 */ }
  } ;
  
  struct Square : Shape
  {
      virtual void draw() { /* 正方形を描画 */ }
  } ;
  
  void f( Shape * ptr )
  {
      ptr->draw() ; // 実行時の型に応じて図形を描画する
  }


ここでは、Shapeクラスというのは、具体的に描画する方法を持たない。そもそも、Shapeクラス自体のオブジェクトを使うことは想定されていない。このように、そのクラス自体は抽象的な概念であり、実体を持たない場合、ピュアvirtual関数を使うことで、共通のインターフェースとすることができる。



他の言語では、この機能を明確にクラスから分離して、「インターフェース」という名前の機能にしているものもある。C++では、抽象クラスも、制限はあるものの、クラスの一種である。



少なくともひとつのピュアvirtual関数を持つクラスは、アブストラクトクラスとなる。ピュアvirtual関数は、virtual関数の宣言に、ピュア指定子を書くことで宣言できる。



.. code-block:: c++
  
  ピュア指定子:
      = 0 


.. code-block:: c++
  
  struct abstract_class
  {
      virtual void f() = 0 ;
  } ;


ピュアvirtual関数には、定義を与えることはできない。



.. code-block:: c++
  
  struct X
  {
      // エラー
      virtual void f() = 0 { } ; 
  }


この、=0という文法は、初期化子や代入式とは、何の関係もない。ただ、C++の文法上、メンバー関数の宣言の中の、=0というトークン列を、特別な意味を持つものとして扱っているだけである。ピュア指定子を記述する位置は、virt-specifierの後である。



.. code-block:: c++
  
  struct Base { int f ; }
  struct abstract_class : Base
  {
      virtual void f() new = 0 ;// virt-specifierの後
  } ;


<p class="editorial-note">
TODO: virt-specifierに対する適切な訳語。これは将来のドラフトで変更されるかもしれない。



アブストラクトクラスは、他のクラスの基本クラスとして使うことしかできない。アブストラクトクラスのオブジェクトは、派生クラスのサブオブジェクトとしてのみ、存在することができる。



.. code-block:: c++
  
  struct abstract_class
  {
      virtual void f() = 0 ;
  } ;
  
  struct Derived : abstract_class
  {
      void f() { }
  } ;


アブストラクトクラスのオブジェクトを、直接作ることはできない。これには、変数や関数の仮引数、new式などが該当する。



.. code-block:: c++
  
  struct abstract_class
  {
      virtual void f() = 0 ;
  } ;
  
  // エラー、abstract_classのオブジェクトは作れない
  void f( abstract_class param )
  {
      abstract_class obj ; // エラー
      new abstract_class ; // エラー
  }


アブストラクトクラスへのポインターやリファレンスは使える。




.. code-block:: c++
  
  struct abstract_class
  {
      virtual void f() = 0 ;
  } ;
  
  // OK、ポインターとリファレンスはよい
  void f( abstract_class *, abstract_class & ) ;


ピュアvirtual関数を継承していて、ファイナルオーバーライダーがピュアvirtual関数である場合も、アブストラクトクラスとなる。これは例えば、アブストラクトクラスから派生されているクラスが、ピュアvirtual関数をオーバーロードしていなかった場合などが、該当する。



.. code-block:: c++
  
  struct Base { virtual void f() = 0 ; } ;
  struct Derived : Base { } ;


この場合、Derivedも、Baseと同じく、アブストラクトクラスになる。



派生クラスによって、ピュアvirtual関数ではないvirtual関数をオーバーライドして、ピュアvirtual関数にすることができる。その場合、派生クラスはアブストラクトクラスとなる。



.. code-block:: c++
  
  struct Base { virtual void f() { } } ;
  struct Derived : Base { virtual void f() = 0 ; } ;
  
  int main()
  {
      Base b ; // OK
      Derived d ; // エラー
  }


この例では、Baseはアブストラクトクラスではない。Derivedはアブストラクトクラスである。



構築中、または破棄中のアブストラクトクラスのコンストラクターやデストラクターの中で、ピュアvirtual関数を呼び出した場合の挙動は、未定義である。



.. code-block:: c++
  
  struct Base
  {
      virtual void f() = 0 ;
  
      // この関数を、Baseのコンストラクターやデストラクターから呼ぶとエラー
      void g()
      { f() ; }
  
      // コンストラクター
      Base() // エラー、未定義の挙動
      { f() ; }
  
      // デストラクター
      ~Base() // エラー、未定義の挙動
      { f() ; }
  } ;
  
  struct Derived : Base
  {
      virtual void f() { }
  
      // Derivedはアブストラクトクラスではないので、問題はない
      Derived() { f() ; }
      ~Derived() { f() ; }
  } ;


