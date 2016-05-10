
public class Analysis {
    public static void main(final String[] args) {

        int N = 10;
        while (N < 500) {
            Stopwatch sw = new Stopwatch();
            Timing.trial(N, 770858);
            double time = sw.elapsedTime();
            System.out.println(String.format("%d %f", N, time));

            N += 100;
        }
    }
}

 for (Board board : twinNode.board.neighbors()) {

            SearchNode n = new SearchNode(board, node.moves + 1, node);
            if (n.equals(twinNode.prev)) {
                continue;
            }

            pqTwin.insert(n);
        }
        Board twin = node.board.twin();
        twinNode = new SearchNode(twin, 0, null);
        pqTwin.insert(twinNode);
        return false;
    }

    /**
     * @return is the initial board solvable?
     */
    public boolean isSolvable() {
        return solvable;
    }