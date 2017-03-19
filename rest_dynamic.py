    def set(self, ps):
        print("set({}) ...".format(ps))
        all_zero = True
        for i in ps:
            if i != 0:
                all_zero = False
            if i < 0:
                return;
        if all_zero:
            print("ALL_ZERO")
            self.array[tuple(ps)] = 1
            return
        value = 0
        for j in range(self.n_dims):
            delta_j_ps = self.delta(j,ps)
            print("delta({}, {}) = {}".format(j,ps,delta_j_ps))
            ps[j] -= 1
            print("  array({}) = {}".format(ps, self.array[tuple(ps)]))
            if self.array[tuple(ps)] == -1:
                self.set(ps)
                pass
            if delta_j_ps == 1:
                value += self.array[tuple(ps)]
            ps[j] += 1
        # print(" ... Setting array({}) to {}".format(ps, value))
        self.array[tuple(ps)] = value

    def fill(self):
        minus_one = np.array(self.dimensions) - 1
        self.set(minus_one)
        print(self.array)
        return self.array[tuple(minus_one)]

"""
    dims = d.dimensions
    minus_one = np.array(dims) - 1

    print("dims : {}".format(dims))
    print("minus_one = {}".format(minus_one))
    print("d.fill() = {}".format(d.fill()))
    ind = np.array([2,2])
    j = 0
    print("d.delta({},{}) = {}".format(j, ind, d.delta(0,ind)))
"""
