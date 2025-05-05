package firstclasscollection;

import java.util.List;

public class NameList {
    private final List<String> names;

    public NameList(List<String> names) {
        this.names = List.copyOf(names);
    }

    public boolean contains(String name) {
        return names.contains(name);
    }
}
