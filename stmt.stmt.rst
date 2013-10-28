文（Statements）
================================================================================

ラベル文（Labeled statement）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  識別子 : 文
  case 定数式 : 文
  default : 文


文にはラベルを付けることができる。ラベルとは、その文を指す識別子である。文にラベルを付けるための文を、ラベル文（label statement）という。ラベル文には、必ず後続する文が存在しなければならない。



.. code-block:: c++
  
  void f()
  {
      label :
  // エラー、ラベルに続く文がない
  } // ブロックの終わり
  
  void g()
  {
  // OK、ラベルに続く文がある
      label_1 :/* 式文 */ ;
      label_2 : {/* 複合文 */} ;
  }


識別子ラベル（identifier label）は、識別子を宣言する。この識別子は、goto文でしか使えない。



.. code-block:: c++
  
  int main()
  {
  label_1 : ;
  label_2 : ;
  label_3 : ;
  
      goto label_2 ;
  } 


ラベルの識別子のスコープは、宣言された関数内である。ラベルを再宣言することはできない。ラベルの識別子は、宣言する前にgoto文で使うことができる。



.. code-block:: c++
  
  // ラベルのスコープは、宣言された関数内
  void f() { label_f : ; }
  vopd g()
  {
      goto label_f ; // エラー、この関数のスコープのラベルではない
  }
  
  // ラベルを再宣言することはできない
  void h()
  {
      label_h : ; // label_hの宣言
      label_h : ; // エラー、ラベルの再宣言はできない
  }
  
  // ラベルの識別子は、宣言する前にgoto文で使うことができる
  void i()
  {
  // 識別子label_iは、この時点では、まだ宣言されていないが、使うことができる
      goto label_i ;
  label_i ;
  }


ラベルの識別子は、独自の名前空間を持つので、他の識別子と混同されることはない。



.. code-block:: c++
  
  int main()
  {
      identifier : ; // ラベルの識別子
      int identifier ; // 変数の識別子
  
      goto identifier ; // ラベルの識別子が使われる
      identifier = 0 ; // 変数の識別子が使われる
  }


caseラベルとdefaultラベルは、switch文の中でしか使うことができない。



.. code-block:: c++
  
  int main()
  {
      switch(0)
      {
          case 0 : ;
          default : ; 
      }
  }


式文（Expression statement）
--------------------------------------------------------------------------------



.. code-block:: c++
  
 

式文（expression statement）とは、式を書く事のできる文である。文の多くは、この式文に該当する。式文は、セミコロン（;）を終端記号として用いる。式文は、書かれている式を評価する。



.. code-block:: c++
  
  int main()
  {
      0 ; // 式は0
      1 + 1 ; // 式は1 + 1
  
      // これは式文ではなく、return文
      return 0 ; 
  }


式文は、式を省略することもできる。式を省略した式文を、null文という。



.. code-block:: c++
  
      /* 式を省略*/ ; // null文
  
      ;;;; // null文が四つ
      ;;;;;;;; // null文が八つ


null文は、評価すべき式がないので、何もしない文である。null文はたとえば、ブロックの終りにラベル文を書きたい場合や、for文やwhile文のようなループを、単に回したい場合などに、使うことができる。



.. code-block:: c++
  
  int main()
  {
      // 単にループを回すだけのfor文
      for ( int i = 0 ; i != 10 ; ++i ) ;
  
  label : ; // ラベル文には、後続する文が必要。
  }


複合文、ブロック（Compound statement or block）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  { ひとつ以上

複合文、またはブロックという文は、文をひとつしか書けない場所に、複数の文を書くことができる文である。



.. code-block:: c++
  
  void f( bool b )
  {
      if ( b )
          /*ここにはひとつの文しかかけない*/ ;
  
      if ( b )
      {
          // いくらでも好きなだけ文を書くことができる。
      }
  }


複合文は、ブロックスコープを定義する。



.. code-block:: c++
  
  int main()
  {// ブロックスコープ
      { // 新たなブロックスコープ
      }
  }


選択文（Selection statements）
--------------------------------------------------------------------------------



選択文は、複数あるフローのうち、どれかひとつを選ぶ文のことである。



もし、選択文の中の文が、複合文ではなかった場合、その文を複合文で囲んだ場合と同じになる。



.. code-block:: c++
  
  void f( bool b )
  {
      if ( b )
          int x ;
  
      x = 0 ; // エラー、xは宣言されていない
  }


このコードは、以下のコードと同等であるため、if文の次の式文で、xという名前を見つけられない。



.. code-block:: c++
  
  void f( bool b )
  {
      if ( b )
      { int x ; }
  
      x = 0 ; // エラー、xは宣言されていない
  }


条件について
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: c++
  
  条件:
      式
      宣言


条件には、式が宣言を書くことができる。条件は、if文やswitch文だけではなく、while文などでも使われる。



.. code-block:: c++
  
  void f()
  {
      if ( true ) ;
      if ( int x = 1 ) ;
  }


条件に宣言を書くことができる理由は、コードを単純にするためである。



.. code-block:: c++
  
  // 何か処理をして結果を返す関数
  int do_something() ;
  
  int main()
  {
      int result = do_something() ;
      if ( result )
      {
          // 処理
      }
  }


条件には宣言を書く事ができるため、以下のように書くことができる。





.. code-block:: c++
  
  if ( int result = do_something() )


if文（The if statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  if ( 条件 ) 文
  if ( 条件 ) 文 else 文


if文は、条件の値によって、実行すべき文を変える。



条件がtrueと評価された場合、一つ目の文が実行される。条件がfalseと評価された場合、elseに続く二つ目の文が有るのならば、二つ目の文が実行される



.. code-block:: c++
  
  int main()
  {
      if ( true ) // 一つ目の文が実行される
          /*一つ目の文*/ ;
  
      if ( false ) // 一つ目の文は実行されない
          /*一つ目の文*/ ;
  
      if ( true ) // 一つ目の文が実行される
          /*一つ目の文*/ ;
      else
          /*二つ目の文*/ ;
  
      if ( false ) // 二つ目の文が実行される
          /*一つ目の文*/ ;
      else
          /*二つ目の文*/ ;
  }


elseは、近い方のif文に対応する。



.. code-block:: c++
  
  int main()
  {
      if ( false ) // #1
          if ( true ) ;// #2
  
      else { } // #2のif文に対応するelse
  }


インデントに騙されてはいけない。インデントを正しく対応させると、以下のようになる。



.. code-block:: c++
  
  int main()
  {
      if ( false ) // #1
          if ( true ) ;// #2
          else ; // #2のif文に対応するelse
  }


このため、elseのあるif文の中に、さらにif文をネストさせたい場合は、内側のif文にも、elseが必要である。



.. code-block:: c++
  
  int main()
  {
      if ( false ) // #1
          if ( true ) ;// #2
          else ; // #2のif文に対応するelse
      else ; // #1のif文に対応するelse
  }


あるいは、ブロック文を使うという手もある。



.. code-block:: c++
  
  int main()
  {
      if ( false ) // #1
      { if ( true ) ; }
  
      else ; // #1のif文に対応するelse
  }




switch文（The switch statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  switch( 条件 ) 文 


switch文は、条件の値によって、実行する文を選択する。



条件は、整数型かenum型、もしくは非explicitな変換関数を持つクラス型でなければならない。条件がクラス型の場合、整数型かenum型に型変換される。



.. code-block:: c++
  
  struct C
  {
      operator int(){ return 0 ; }
  } ;
  
  int main()
  {
      switch(1) ; // OK
      C c ;
      switch(c) ; // OK、C::operator int()が呼ばれる
  
      switch(1.0) ; // エラー、浮動小数点数型は指定できない
  
      switch( static_cast<int>(1.0) ) ; // OK
  }


switch文の中の文には、通常、複合文を指定する。複合文の中には、caseラベル文やdefaultラベル文を書く。



.. code-block:: c++
  
  switch(1)
  {
      case 1 :
          /* 処理 */ ;
      break ;
  
      case 2 :
          /* 処理 */ ;
      break ;
  
      default :
          /* 処理 */ ;
  }


caseラベル文に指定する式は、整数の定数式でなければならない。また、同じswitch内で、caseラベル文の値が重複してはならない。



defaultラベル文は、switch文の中の文に、ひとつだけ書くことができる。



switch文が実行されると、まず条件が評価される。結果の値が、switch文の中にあるcaseラベルに対して、ひとつづつ比較される。もし、値が等しいcaseラベル文が見つかった場合、そのラベル分に実行が移る。



.. code-block:: c++
  
  void f( int const value )
  {
      switch( value )
      {
          case 1 :
              std::cout << "Good morning." << std::endl ;
          break ;
          case 2 :
              std::cout << "Good afternoon." << std::endl ;
          break ;
          case 3 :
              std::cout << "Good evening." << std::endl ;
          break ;
      }
  }
  
  int main()
  {
      f( 1 ) ; // Good morning.
      f( 2 ) ; // Good afternoon.
      f( 3 ) ; // Good evening.
  }


条件と値の等しいcaseラベルが見つからない場合で、defaultラベルがある場合、defaultラベルに実行が移る。



.. code-block:: c++
  
  void f( bool const value )
  {
      switch( value )
      {
          case true :
              std::cout << "true" << std::endl ;
          break ;
  
          default :
              std::cout << "false" << std::endl ;
          break ;
      }
  }
  
  int main()
  {
      f( true ) ; // true
      f( false ) ; // false
  }


条件と値の等しいcaseラベルが見つからず、defaultラベルもない場合、switch内の文は実行されない。



.. code-block:: c++
  
  int main()
  {
      // switch内の文は実行されない
      switch( 0 )
      {
          case 999 :
              std::cout << "hello" << std::endl ;
          break ;
          case 123456 :
              std::cout << "hello" << std::endl ;
          break ;
      }
  }


caseラベルとdefaultラベル自体には、文の実行を変更する機能はない。



.. code-block:: c++
  
  void f( int const value )
  {
      switch( value )
      {
          case 1 :
              std::cout << "one" << std::endl ;
          default :
              std::cout << "default" << std::endl ;
          case 2 :
              std::cout << "two" << std::endl ;
      }
  }


この場合、valueの値が1の場合、case 1のラベル文に続く文も、すべて実行されてしまう。また、valueの値が1でも2でもない場合、defaultラベル文に続くcase 2のラベル文も、実行されてしまう。このため、switch内の実行を切り上げたい時点で、<a href="#stmt.break">break文</a>を書かなければならない。break文を書き忘れたことによる、意図しない文の実行は、よくあることなので、注意が必要である。なお、このことは、逆に利用することもできる。



.. code-block:: c++
  
  void f( int const value )
  {
      switch( value )
      {
          case 3 :
          case 5 :
          case 7 :
              /* 何らかの処理 */ ;
      }
  }


この例では、valueの値が3, 5, 7のいずれかの場合に、何らかの処理が実行される。




繰り返し文（Iteration statements）
--------------------------------------------------------------------------------



繰り返し文（Iteration statements）は、ループを書くための文である。



繰り返し文の中の文は、暗黙的に、ブロックスコープを定義する。このブロックスコープは、文の実行のループ一回ごとに、出入りする。例えば、



.. code-block:: c++
  
  while( true )
      int i ;


という文は、以下のように書いたものとみなされる。



.. code-block:: c++
  
  while( true )
  { int i ; }


従って、繰り返し文の中の変数は、ループが回されるごとに、生成、破棄されることになる。



.. code-block:: c++
  
  struct C
  {
      C(){ std::cout << "constructed." << std::endl ; }
      ~C(){ std::cout << "destructed." << std::endl ; }
  } ;
  
  int main()
  {
      while( true )
      { // 生成、破棄を繰り返す
          C c ;
      }
  }


while文（The while statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  while ( 条件 ) 文


while文は、条件の結果がfalseになるまで、文を繰り返し実行する。条件は、文の実行前に、繰り返し評価される。



.. code-block:: c++
  
  int main()
  {
      // 一度も繰り返さない
      while ( false )
      {
          std::cout << "hello" << std::endl ; 
      }
  
      // 無限ループ
      while ( true )
      {
          std::cout << "hello" << std::endl ; 
      }
  
      // iが10になるまで繰り返す
      int i = 0 ;
      while ( i != 10 )
      {
          ++i ;
      }
  
  }


条件が宣言である場合、変数のスコープは、while文の宣言された場所から、while文の最後までである。条件の中で宣言された変数は、文の実行が繰り返されるたびに、生成、破棄される。



.. code-block:: c++
  
  while ( T t = x ) 文


という文は、



.. code-block:: c++
  
  label:
  {
      T t = x;
      if (t) {
          statement
          goto label;
      }
  }


と書くのに等しい。




do文（The do statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  do 文 while ( 式 ) ;


do文の式は、boolに変換される。boolに変換できない場合、エラーとなる。



do文は、式の結果がfalseになるまで、文が繰り返し実行される。ただし、式の評価は、文の実行の後に行われる。



.. code-block:: c++
  
  int main()
  {
      // 一度だけ文を実行
      do {
          std::cout << "hello" << std::endl ; 
      } while ( false ) ;
  
  
      // 無限ループ
      do {
          std::cout << "hello" << std::endl ; 
      } while ( true ) ;
  }




for文（The for statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: c++
  
  for ( for初期化文 

for文は、for初期化文で、ループ前の初期化を書き、条件で、ループを実行するかどうかの判定を行い、文が実行されたあとに、そのつど式が評価される。



for文の実行では、まず、for初期化文が実行される。for初期化文は、式文か、変数の宣言を行うことができる。変数のスコープは、for文の最後までである。次に、文の実行の前に、条件が評価され、falseとなるまで文が繰り返し実行される。文の実行の後に、式が評価される。



.. code-block:: c++
  
  for ( for初期化文 条件 ; 式 ) 文


は、以下のコードと同等である。



.. code-block:: c++
  
  {
      for初期化文
      while ( 条件 ) {
          文
          式 ;
      }
  }


ただし、文の中でcontinue文を使ったとしても、式は評価されるという違いがある。



for文は、while文でよく書かれるコードを書きやすくした構文である。例えば、while文を10回実行したい場合、



.. code-block:: c++
  
  int main()
  {
      // カウンター用の変数の宣言
      int i = 0 ; 
  
      while ( i != 0 )
      {
          // 処理
          ++i ;
      }
  }


このようなコードを書く。for文は、このようなコードを、一度に書けるようにしたものである。



.. code-block:: c++
  
  int main()
  {
      for ( int i = 0 ; i != 0 ; ++i )
      {
          // 処理
      }
  }


for文の条件と式は、省略することができる。条件を省略した場合、trueとみなされる。



.. code-block:: c++
  
  int main()
  {
      // 条件を省略、for ( ; true ; ) と同じ
      for ( ; ; ) ;
  }




range-based for文（The range-based for statement）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



TODO: Madrid meeting後に変更する。ADL baseではなくtraits baseになる予定。



ここでは、range-based forの言語機能を説明している。ライブラリとしてのレンジや、ユーザー定義のクラスでレンジをサポートする方法については、ライブラリの<a href="#iterator.range">レンジ</a>を参照。



range-based forの基本
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  for ( for-range-宣言 : for-range-初期化子 ) 文


range-based forは、レンジをサポートしている配列、初期化リスト、クラスの各要素に対して、それぞれ文を実行するための文である。



range-based forは、forに続けて、括弧を書く。括弧の中には、変数の宣言と、レンジとを、:で区切る。



.. code-block:: c++
  
  int main()
  {
      int a[] = { 1, 2, 3 } ;
      for( int i : a ) ; // 各要素をint型のコピーで受ける
      for ( int & ref : a ) ; // 各要素をリファレンスで受ける
      for ( auto i : a ) ; // auto指定子を使った例
  }


このようにして宣言した変数は、range-based for文の中で使うことができる。range-based for文は、変数をレンジの各要素で初期化する。



.. code-block:: c++
  
  int main()
  {
      int a[] = { 1, 2, 3 } ;
      for ( auto i : a )
      {
          i ;
      }
  }


この例では、ループは3回実行され、変数iの値は、それぞれ、1, 2, 3となる。



ループを使ってコードを書く場合、配列やコンテナーの各要素に対して、それぞれ何らかの処理をするという事が多い。



.. code-block:: c++
  
  #include <iostream>
  
  int main()
  {
      int a[5] = { 1, 2, 3, 4 ,5 }  ;
      for (
          int * iter = &a ; // 各要素を表す変数の宣言
          iter != &a + 5 ; // 終了条件の判定
          ++iter // 次の要素の参照
      )
      {
          // 各要素に対する処理
          std::cout << *iter << std::endl ;
      }
  }


しかし、このようなループを正しく書くのは、至難の業である。なぜならば、人間は間違いを犯すからである。しかし、このようなループは、誰が書いても、概ね似たようなコードになる。range-based forを使えば、このような冗長なコードを省くことができる。



.. code-block:: c++
  
  int main()
  {
      int a[5] = { 1, 2, 3, 4 ,5 }  ;
      for ( auto i : a )
      {
          std::cout << i << std::endl ;
      }
  }


range-based forは、極めて簡単に使うことができる。for-range-宣言で、各要素を得るための変数を宣言する。for-range初期化子で、レンジをサポートした式を書く。文で、各要素に対する処理を書く。



.. code-block:: c++
  
  int main()
  {
      int a[5] = { 1, 2, 3, 4 ,5 }  ;
      for ( int & i : a )
      {
          i *= 2 ; // 二倍する
      }
  }


この例では、配列aの各要素は、二倍される。配列の要素を書き換えるために、変数は参照で受けている。



range-based forには、配列の他にも、初期化リストや、レンジをサポートしたクラスを書く事ができる。STLのコンテナーは、レンジをサポートしている。配列以外にrange-based forを適用する場合、&lt;iterator&gt;の#includeが必要である。



.. code-block:: c++
  
  #include <iterator>
  
  int main()
  {
      // 配列
      int a[] = { 1, 2, 3 } ;
      for ( auto i : a )
      { std::cout << i << std::endl ; }     
      
      // 初期化リスト
      for ( auto i : { 1, 2, 3 } )
      { std::cout << i << std::endl ; } 
  
      // クラス
      std::vector<int> v = { 1, 2, 3 } ;
      for ( auto i : v )
      { std::cout << i << std::endl ; } 
  }




range-based forの詳細
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



<p class="editrial-note">
TODO:メンバー関数begin/end優先の追記。



range-based forは、本来、コンセプトという言語機能と共に提供される予定であった。しかし、コンセプトは紆余曲折を経た結果、C++11では却下された。そのため、現行のrange-based forは、コンセプトではなく、ADLによる実装をされている。



以下のrange-based for文があるとする。



.. code-block:: c++
  
  for ( for-range-宣言 : for-range-初期化子 ) 文


このrange-based for文は、以下のように変換される。



for-range-初期化子が式の場合、括弧でくくられる。これは、コンマ式が渡されたときに、正しく式を評価するためである。



.. code-block:: c++
  
  for ( auto i : a, b, c, d ) ;
  // 括弧でくくる
  for ( auto i : (a, b, c, d) ) ;


for-range-初期化子が初期化リストの場合、なにもしない。



.. code-block:: c++
  
  {
      // 式の結果をlvalueかrvalueのリファレンスで束縛
      auto && __range = for-range-初期化子 ;
      for (
          auto __begin = begin式, // 先頭のイテレーター
          __end = end式 ; // 終端のイテレーター
          __begin != __end ; // 終了条件
          ++__begin ) // イテレーターのインクリメント
      {
          for-range-宣言 = *__begin; // 要素を得る
          文
      }
  }


ここでの、__range、__begin、__endという変数は、説明のための仮の名前である。実際のrange-based for文の中では、このような変数名は存在しない。



__rangeとは、for-range-初期化子の式の結果を保持するためのリファレンスである。auto指定子とrvalueリファレンスの宣言子が使われていることにより、式のlvalue、rvalue、CV修飾子をいかんを問わずに、結果をリファレンスとして束縛できる。



begin式とend式は、先頭と終端へのイテレーターを得るための式である。



for-range-初期化子の型が、配列の場合、begin式は「__range」となり、end式は、「__range + 配列の要素数」となる。



.. code-block:: c++
  
  int x [10] ;
  for ( auto i : x )
  {
      // 処理
  }


上記のrange-based for文は、以下のように変換される。



.. code-block:: c++
  
  int x [10] ;
  {
      auto && __range = ( x ) ;
      for (
          auto __begin = __range,
          __end = __range + 10 ;
          __begin != __end ;
          ++__begin )
      {
          auto i = *__begin; 
          // 処理
      }
  }


型が配列以外の場合、begin式は「begin(__range)」に、end式は「end(__range)」に変換される。



.. code-block:: c++
  
  std::vector<int> v ;
  for( auto i : v )
  {
      // 処理
  }


.. code-block:: c++
  
  std::vector<int> v ;
  {
      // 式の結果をlvalueかrvalueのリファレンスで束縛
      auto && __range = ( v ) ;
      for (
          auto __begin = begin(__range),
          __end = end(__range) ;
          __begin != __end ;
          ++__begin )
      {
          auto i = *__begin; 
          // 処理
      }
  }


ここでのbegin(__range)とend(__range)は、関数呼び出しである。ただし、この名前の解決には、通常の名前探索のルールは用いられない。begin/endの名前探索には、関連名前空間に特別にstdを加えた、ADLによってのみ名前探索される。通常のunqualified名前探索は用いられない。<a href="#basic.lookup.argdep">ADL</a>の詳細については、詳しい説明を別に設けてあるので、そちらを参照。






ジャンプ文（Jump statements）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



ジャンプ文は、実行する文を無条件で変更するための文である。



break文（The break statement）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  break ;


break文は、繰り返し文かswitch文の中で使うことができる。break文は、最も内側の繰り返し文かswitch文から、抜け出す機能を持つ。もし繰り返し文かswitch文に続く、次の文があれば、実行はその文に移る。break文は、ループを途中で抜けたい場合に使うことができる。



.. code-block:: c++
  
  int main()
  {
      while( true )
      {
          break ;
      }
  
      do
      {
          break ;
      } while ( true ) ;
  
      for ( ; ; )
      {
          break ;
      }
  
      switch(0)
      {
          default :
              break ;
      }
  }


break文によって抜ける繰り返し文かswitch文とは、break文が書かれている場所からみて、最も内側の文である。



.. code-block:: c++
  
  int main()
  {
      while( true ) // 外側
          while ( true ) // 内側
          {
              break ;
          }
  }


break文が使われている内側の文からは抜けるが、外側の文から抜けることはできない。




continue文（The continue statement）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  continue ;


continue文は、繰り返し文の中で使うことができる。continue文を実行すると、そのループの実行を中止する。



while文やdo文の場合、条件が評価され、その結果次第で、次のループが再び始まる。for文の場合は、ループの最後に必ず行われる式が、もしあれば評価され、条件が評価され、その結果次第で、次のループが再び始まる。



.. code-block:: c++
  
  int main()
  {
      while( true )
      {
          continue ;
      }
  
      do
      {
          continue ;
      } while ( true ) ;
  
      for ( int i = 0 ; true ; ++i )
      {
          continue ;// for文の式である++iが評価される。
      }
  }


continue文に対する繰り返し文とは、continue文が書かれている場所からみて、最も内側の繰り返し文のループである。



.. code-block:: c++
  
  int main()
  {
      while ( true ) // 外側
          while ( true ) // 内側
          {
              continue ;
          }
  
  }


この例では、continue文は、内側のwhile文のループを中止する。ただし、continue文はbreak文とは違い、繰り返し文から抜け出すわけではないので、内側のwhile文の実行が続く。




return文（The return statement）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  return

return文は、関数の呼び出し元に実行を戻す文である。



.. code-block:: c++
  
  int f()
  {
      return 0 ; // OK
      return ; // エラー、戻り値がない
  }


return文の式は、関数の呼び出し元に、戻り値として返される。式は関数の戻り値の型に暗黙的に変換される。変換できない場合はエラーとなる。



戻り値を返さない関数の場合、return文の式は省略できる。戻り値を返さない関数とは、戻り値の型がvoid型の関数、コンストラクター、デストラクターである。



.. code-block:: c++
  
  struct C
  {
      C() { return ; }
      ~C() { return ; }
  } ;
  
  void f() { return ; }


戻り値を返さない関数の場合は、return文で戻り値を返してはならない。



.. code-block:: c++
  
  void f()
  {
      return ; // OK
      return 0 ; // エラー、関数fは戻り値を返さない
  }


ただし、return文の式がvoidと評価される場合は、戻り値を返していることにはならない。



.. code-block:: c++
  
  void f() { }
  void g()
  {
      // 関数fの呼び出しの結果は、void
      return f() ;
  }


関数の本体の最後は、値を返さないreturn文が書かれたことになる。



.. code-block:: c++
  
  void f()
  {
  // 値を返さないreturn文が書かれた場合と同じ
  }


値を返す関数で、return文が省略された場合の挙動は未定義である。ただし、main関数だけは、特別に0が返されたものとみなされる。



.. code-block:: c++
  
  // 値を返す関数
  int f( bool b )
  {
      if ( b ) 
      { return 0 ; }
  // bがfalseの場合の挙動は未定義
  }
  
  int main()
  {
  // return 0 ;が書かれた場合と同じ
  }


return文には、初期化リストを書くことができる。



.. code-block:: c++
  
  std::initializer_list<int> f()
  {
      return { 1, 2, 3 } ;
  }
  
  struct List
  {
      List( std::initializer_list<int> ) { }
  } ;
  
  List g()
  {
      return { 1, 2, 3 } ;
  }


return文は、関数の戻り値の為に、一時オブジェクトを生成するかもしれない。一時オブジェクトを生成する場合、値はコピーかムーブをしなければならないが、return文では、コピーかムーブかの選択のために、式をrvalueとみなす可能性もある。式をrvalueとみなすということは、lvalueであっても、暗黙的にムーブされる可能性があることを意味する。これは例えば、「return文を実行して関数の呼び出し元に戻った場合、関数のローカル変数は破棄されるためムーブしてもかまわない」という状況で、コピーではなく、ムーブを選択できるようにするためである。



.. code-block:: c++
  
  // コピーとムーブが可能なクラス
  struct C
  {
      C() = default ; // デフォルトコンストラクター
      C( C const & ) = default ; // コピーコンストラクター
      C( C && ) = default ; // ムーブコンストラクター
  } ;
  
  C f()
  {
      C c ;
      // 一時オブジェクトが生成される場合、コピーかムーブが行われる。
      return c ; 
  // なぜならば、ローカル変数はreturn文の実行後、破棄されるので、ムーブしても構わないからである。
  }


また、上記のコードで、一時オブジェクトが生成されない場合もある。これはインライン展開やフロー解析などによる最適化の結果、コピーもムーブも行わなくてもよいと判断できる場合、そのような最適化を許可するためである。




goto文（The goto statement）
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



.. code-block:: c++
  
  goto 識別子 ;


goto文は、関数内のラベル文に無条件で実行を移すための文である。同じ関数内であれば、どこにでもジャンプできる。



.. code-block:: c++
  
  int main()
  {
  label : ; // labelという名前のラベル文
  
      goto label ;
  }


宣言文の前にジャンプする。あるいは、宣言文を飛び越すことについては、宣言文の項目で詳しく解説している。






宣言文（Declaration statement）
--------------------------------------------------------------------------------



.. code-block:: c++
  
  ブロック宣言 ;


宣言文は、あるブロックの中に、新しい識別子を導入するための文である。ブロック宣言や、その他の宣言についての詳細は、宣言、宣言子、クラスを参照。



.. code-block:: c++
  
  int main()
  {
      int a ; // int型の識別子aという変数の宣言
  
      void f(void) ; // void (void)型の識別子fという関数の宣言
  
  }


<a href="#basic.stc.auto">自動ストレージの有効期間</a>を持つ変数は、宣言文が実行されるたびに、初期化される。また、宣言されているブロックから抜ける際に、破棄される。



.. code-block:: c++
  
  struct Object
  {
      Object()
      { std::cout << "constructed." << std::endl ;}
      ~Object()
      { std::cout << "destructed." << std::endl ;}
  } ;
  
  int main()
  {
      {
          Object object ; // 生成
      } // ブロックスコープから抜ける際に破棄される
  }


ジャンプ文を使えば、宣言文の後から前に実行を移すことが可能である。その場合、宣言文によって生成されたオブジェクトは破棄され、宣言文の実行と共に、再び生成、初期化される。



.. code-block:: c++
  
  struct Object
  {
      Object()
      { std::cout << "constructed." << std::endl ;}
      ~Object()
      { std::cout << "destructed." << std::endl ;}
  } ;
  
  int main()
  {
  label :
      Object object ; // 変数objectが生成、初期化される
  
      goto label ; // 変数objectは破棄される
  }


この例では、Objectクラスの変数objectは、gotoで宣言文の前にジャンプするたびに、破棄されることになる。



goto文やswitch文などのジャンプ文を使えば、自動変数の宣言文を実行せずに、通り越すコードが書ける。



.. code-block:: c++
  
  // goto文の例
  void f()
  {
      // labelという名前のラベル文にジャンプする
      goto label ;
  
      int value ; // 自動変数の宣言文
  
  label : ;
  // valueの宣言文を、実行せずに通り越してしまった。
  }
  
  // switch文の例
  void g( int value )
  {
      switch ( value )
      {
          int value ; // 変数の宣言文
  
          // 宣言文を飛び越えてしまっている。
          case 0 : break ;
          case 1 : break ;
          default : break ;
      }
  }


このようなコードは、ほぼすべての場合、エラーとなるので、書くべきではない。では、変数の宣言文を通り越してもエラーとならない場合は何か。これは、相当の制限を受ける。まず、変数の型は、スカラー型か、trivialなデフォルトコンストラクターとtrivialなデストラクターを持つクラス型でなければならない。また、そのような型にCV修飾子を加えた型と、配列型でもよい。その上で、初期化子が存在していてはならない。



.. code-block:: c++
  
  struct POD { } ;
  // trivialではないコンストラクターを持つクラス
  struct Object { Object() {} } ;
  
  int main()
  {
      // 変数の宣言文を飛び越えるgoto文
      goto label ;
  
      // エラー
      // 変数の型はスカラー型だが、初期化子がある。
      int value = 0; 
  
      int scalar ; // OK
  
      // エラー
      // 変数のクラス型がtrivialではないコンストラクターを持っている
      Object object ;
  
      POD pod ; // OK
  
  label : ;
  }


すべてのstatic変数とthread_local変数は、他のあらゆる初期化に先立って、ゼロ初期化される。



.. code-block:: c++
  
  int main()
  {
      goto label ;
      static int value ; // static変数は必ずゼロ初期化される
  label : 
      // この場合、valueは0であることが保証されている
      if ( value == 0 ) ;
  }


ブロックスコープ内のstatic変数とthread_local変数は、定数初期化による早期の初期化が行われない場合、宣言に始めて処理が到達した際に、初期化される。



.. code-block:: c++
  
  // 定数初期化できない型
  struct X
  {
      int member ;
      X( int value ) : member( value ) { }
  } ;
  
  void f()
  {
      // xのゼロ初期化はすでに行われている
      static X x(123) ;
      // この時点で、xの初期化は完了している。
  }


ブロックスコープ内のstatic変数とthread_local変数が定数初期化されている場合、実装は早期に初期化を行なってもかまわない。ただし、行われるという保証はない。



.. code-block:: c++
  
  // 定数初期化できる型
  struct X
  {
      int member ;
      constexpr X( int value ) : member(value) { }
  } ;
  
  // 定数初期化できない型
  struct Y
  {
      int member ;
      Y ( int value ) : member(value) { }
  } ;
  
  int g()
  {
      goto label ; // 宣言文を飛び越してしまっている。
  
      // constexpr指定子が使われていないことに注意
      // xはstatic変数であり、constexprコンストラクターを使っているため、定数初期化である
      static X x( 123 ) ;
      // constexprコンストラクターを使っていないため、定数初期化ではない
      static Y y( 123 ) ;
  
  label : 
      // xは初期化されているかもしれないし、初期化されていないかもしれない
      // yは初期化されていない
      // 両方とも、ゼロ初期化は保証されている
  }


この例では、関数gのstaticローカル変数xとyの宣言文には、処理が到達しない。そのため、xとyが初期化されている保証はない。ただし、xは定数初期化なので、実装によっては、早期初期化されている可能性がある。ゼロ初期化だけは常に保証されている。





static変数とthread_local変数は、宣言文の実行のたびに初期化されることはない。



.. code-block:: c++
  
  int f( int x )
  {
      // 一回だけ初期化される
      // 定数初期化なので、いつ初期化されるかは定められていない
      // ただし、ゼロ初期化はすでに行われている
      static int value = 1 ;
      // この時点で、初期化は完了していることが保証されている
   
      int temp = value ;
      value = x ;
  
      return temp ;
  }
  
  int main()
  {
      f(2) ; // 1
      f(3) ; // 2
      f(4) ; // 3
  }


もし、static変数とthread_local変数の初期化が、例外がthrowされたことにより終了した場合は、初期化は未完了だとみなされる。そのような場合、次に宣言文を実行した際に、再び初期化が試みられる。



.. code-block:: c++
  
  int flag = 0 ;
  
  struct X
  {
      X()
      {
          if ( flag++ == 0 )
              throw 0 ;
      }
  
  } ;
  
  void f()
  {
      static X x ;
  }
  
  int main()
  {
      try
      {
          f() ; // 関数fのstaticローカル変数xの初期化は未完了
      }
      catch( ... ) { }
      f() ; // 関数fのstaticローカル変数xの初期化完了
  
  }


もし、static変数とthread_local変数の宣言文の初期化が再帰した場合、挙動は未定義である。



.. code-block:: c++
  
  int f( int i )
  {
      static int s = f(2*i); // エラー、初期化が再帰している
      return i+1;
  }


この例では、static変数sの初期化が終わらなければ、関数fはreturn文を実行できない。しかし、sの初期化は、再帰している。この場合、挙動は未定義である。


曖昧解決（Ambiguity resolution）
--------------------------------------------------------------------------------



関数形式のキャストを用いた式文と、宣言文とは、文法が曖昧になる場合がある。その場合、宣言文だと解釈される。



.. code-block:: c++
  
  int main()
  {
      int x = 0 ;
  // 不必要な括弧がついた宣言文？　それともキャスト？
      int(x) ;
  }


この場合、int(x) ;という文は、キャストを含む式文ではなく、宣言文になる。したがって、上記の例は、変数xの再定義となるので、エラーである。


