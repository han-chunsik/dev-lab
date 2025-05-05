# 일급 컬렉션 성능 실험

> **JMH(Java Microbenchmark Harness)란?**  
> @Benchmark 애노테이션만으로 메서드 성능을 정밀하게 측정할 수 있는 도구로, JIT 최적화와 GC의 영향을 줄이기 위해 별도 JVM 실행(fork), 워밍업(warmup) 반복 후 본 측정(iteration)
을 수행하며, 측정 결과는 평균값, 표준편차 등 통계로 자동 분석 가능

## 목적
객체 생성/메서드 접근 등의 오버헤드가 실제 실행 시간에 유의미한 영향이 있는지 실험

## 실험 조건
- 벤치마크 도구: JMH
- JDK: 17
- 측정 방식: @BenchmarkMode(Mode.AverageTime)
- 반복 설정:
  - 워밍업: 5회
  - 측정 반복: 10회
  - fork 수: 2 (JVM 분리)
  - 시간 단위: 나노초(ns)

## 비교 대상
- **PlainListBenchmark**: 일반 List<String> 사용, List.contains() 직접 호출
- **FirstClassCollectionBenchmark**: 불변 일급 컬렉션 NameList 객체 사용, 내부에서 동일한 List.contains() 호출

## 분석 방법
- contains("bird500"): 존재하는 값 탐색
- contains("albatross"): 존재하지 않는 값 탐색
=> 두 벤치마크 클래스의 결과 Score 및 Error 비교, 반복 실행을 통해 일관된 성능 차이가 있는지 확인

## 실행 방법
> 작업 폴더: `java-performance`
> Gradle 기반 JMH 실행
```shell
./gradlew jmh
```

## 결과 및 결론
```shell
Benchmark                                   Mode  Cnt    Score    Error  Units
FirstClassCollectionBenchmark.containsHit   avgt   20  539.815 ± 30.725  ns/op
FirstClassCollectionBenchmark.containsMiss  avgt   20  571.956 ± 15.365  ns/op
PlainListBenchmark.containsHit              avgt   20  539.556 ± 19.600  ns/op
PlainListBenchmark.containsMiss             avgt   20  588.353 ± 33.157  ns/op
```
- 일급 컬렉션을 사용하더라도 성능 손해는 미비한 수준
- 내부 로직이 같다면 객체를 한 번 감싼 구조는 성능에 거의 영향 없음
- 따라서 설계상의 장점(불변성, 캡슐화)을 위해 일급 컬렉션을 사용하는 건 충분히 정당화됨
