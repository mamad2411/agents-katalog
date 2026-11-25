---
alwaysApply: true
---

# Juego Android

Quiero crear un juego en Android Studio con Kotlin. La idea es un juego llamado "Mi primer huerto" la idea es similar a la de el famoso juego Pou, donde tienes
la responsabilidad de cuidar "algo" en este caso será a plantas. El juego está destinado a niños de primaria con el fin de que aprendan un poco sobre ciencias naturales
(en como son las fases del crecimiento de las plantas, cómo se ve visualmente, qué pasa si no la cuidan, riegan, etc)

La idea que tengo es la siguiente
Pantallas:
1. Un tipo loading screen donde se muestre el logo del juego y una barra de progreso de "cargando" esta barra lo ideal es que sea personalizada, que se rellene de color verde y poder añadir animaciones de plantas o algo alrededor de la barra.
2. La segunda pantalla (si se inicia la app por primera vez) deberá solicitar al usuario su nombre y su sexo, en esta parte el sexo se elige escogiendo un personaje ya sea jardinero o jardinera, en vez de hacer la selección como tal en un tipo selector, quiero que elijan directamente la imagen.
3. Luego aquí en la 3er pantalla ya se muestra el "Home", donde en medio de la pantalla debe ir una maceta vacia, ahí es donde empieza como tal el juego, el niño debe plantar ahí una semilla de 3 opciones iniciales y en un futuro agregar mas, estas semillas son (frijol, rabano y lechuga). Entonces al inicio del juego cuando se juega por primera vez, se solicita al niño que elija cual quiere usar por primera vez y al escoger intentar hacer una animación de que se plantó esa semilla y ponerla en la maceta. En la misma pantalla de home deberían haber otros elementos como una manguera para el agua, un fertilizante, de fondo que se vea un fondo de un atardecer si es de tarde (aquí usar el reloj del sistema para decidiar que fondo poner, si son las 9 pm por ejemplo, que el fondo se cambie a uno de noche). También en algún lado que consideres correcto agregar barras de estado de la planta, una que sea la vida, otro que sea el nivel de agua. También que haya en la pantalla home otros botones o partes para acceder a otros lugares por ejemplo a una tienda para comprar mas semillas de otras plantas, un icono de "?" donde al dar clic se muestre información importante de la planta plantada.

Otra idea es que al regar la planta o poner fertilizante o controlar alguna plaga que le salga, que el niño al hacer esto, el juego le de puntos y aparezcan en alguna parte en la parte superior, luego otro botón para ajustes y cosas asi. 

La idea del juego es que la planta se divida en etapas, cada etapa la planta tendrá un aspecto diferente, por ejemplo, semilla, joven, maduro, cosechable (en caso de semillas de verduras) las plantas que sean como girasoles, rosas o asi que son mas visuales pues solo dejarlas ahí para siempre, pero las que son cosechables esas desaparecen de la maceta una vez llegada a su etapa mas alta.

Si el niño no riega su planta o la descuida esta se empieza a poner "fea" hasta el punto de morir y el niño debe limpiar los restos. La vida de la planta debe ir disminuyendo mientras el agua esté baja o cuando haya plaga y no se atienda. obviamente hacer esto de una forma pensada, ir disminuyendo poco a poco la vida en intervalos de tiempo coherentes. También por ejemplo podemos definir que cada planta tenga su tiempo de crecimiento definido, por ejemplo no se, el frijol tarda 10 días, y no queremos que el niño espere 10 días, podemos convertir que 1 hora en la vida real sea 1 dia en el juego. Y en la pantalla Home igualmente poner en que etapa está la planta y añadir un contador de cuanto tiempo le queda para la etapa sioguiente

Quiero implementar notificaciones por separado. Por ejemplo 1 cuando la planta llegue al 50% de agua avisar que necesita agua, otra cuando llegue al 25, hacer la notificación mas ruda y avisar también cuando la planta murió. Igual si la planta le salió plaga avisar por notificación.

COn los puntos que se ganan se podrán comprar mas semillas de la tienda o fertilizantes. Los fertilizantes mejoran la salud de la planta, aumentando su vida en caso de que esta se encuentre baja rápidamente, la otra manera pues es que la planta vaya subiendo su vida automáticamente pero será mas lento, entonces el fertilizante lo hace que se haga mas rápido.

a. La aplicación deberá de utilizar diferentes layouts para distribuir de la mejor forma posible
la información y justificar su uso.
b. La aplicación deberá de utilizar de forma correcta cada control utilizado.
c. Deberá de crear controles personalizados que faciliten el desarrollo de la aplicación.
d. El uso de widgets queda opcional y depende del tipo de aplicación.
e. El uso de gráficos en Android es obligatorio.
f. Considere el uso de diferentes sensores, con el propósito de crear mayor interacción y
motivación para el uso de su aplicación.
g. La aplicación deberá de guardar el progreso individual en medios locales.

# Tecnologías
Estas son las tecnologías que usaremos:
1. Jetpack Compose como sistema de interfaces
2. Kotlin como lenguaje de programación
3. Material 3 como sistema de diseño

# Reglas extra
- Siempre que termines de generar un código, compilalo para ver que no hay problemas, para ello utiliza compileDebugKotlin