public class TestJava {
    // presume: d > 0              ; integer "d" must be positive
    // presume: s.length() > 0     ; string "s" must be non-emtpy
    // presume: s.startsWith('a')
    public TestJava(String s, int d) {

    }

    public static void main(String[] args) {
        try {
            TestJava("Hello World", 0);
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    // presume: x >= 0
    public int test(int x) {
        return x*x;
    }
}
