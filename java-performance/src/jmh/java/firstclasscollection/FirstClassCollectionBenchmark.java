package firstclasscollection;

import org.openjdk.jmh.annotations.*;

import java.util.List;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Thread)
public class FirstClassCollectionBenchmark {

    private NameList nameList;

    @Setup(Level.Iteration)
    public void setup() {
        nameList = new NameList(generateBirds());
    }

    private List<String> generateBirds() {
        return java.util.stream.IntStream.range(0, 1000)
                .mapToObj(i -> "bird" + i)
                .toList();
    }

    @Benchmark
    public boolean containsHit() {
        return nameList.contains("bird500");
    }

    @Benchmark
    public boolean containsMiss() {
        return nameList.contains("albatross");
    }
}
