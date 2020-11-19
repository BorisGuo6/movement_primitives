import numpy as np
import pytransform3d.rotations as pr


class SpringDamper:
    def __init__(self, n_dims, dt=0.01, k=1.0, c=None, int_dt=0.001):
        self.n_dims = n_dims
        self.dt = dt
        self.k = k
        self.c = c
        self.int_dt = int_dt

        self.last_t = None
        self.t = 0.0
        self.start_y = np.zeros(self.n_dims)
        self.start_yd = np.zeros(self.n_dims)
        self.start_ydd = np.zeros(self.n_dims)
        self.goal_y = np.zeros(self.n_dims)
        self.initialized = False
        self.current_y = np.zeros(self.n_dims)
        self.current_yd = np.zeros(self.n_dims)
        self.configure()

    def configure(self, last_t=None, t=None, start_y=None, start_yd=None, start_ydd=None, goal_y=None):
        if last_t is not None:
            self.last_t = last_t
        if t is not None:
            self.t = t
        if start_y is not None:
            self.start_y = start_y
        if start_yd is not None:
            self.start_yd = start_yd
        if start_ydd is not None:
            self.start_ydd = start_ydd
        if goal_y is not None:
            self.goal_y = goal_y

    def step(self, last_y, last_yd, coupling_term=None):
        self.last_t = self.t
        self.t += self.dt

        if not self.initialized:
            self.current_y = np.copy(self.start_y)
            self.current_yd = np.copy(self.start_yd)
            self.initialized = True

        self.current_y[:], self.current_yd[:] = spring_damper_step(
            self.last_t, self.t,
            last_y, last_yd,
            self.goal_y,
            self.k, self.c,
            coupling_term=coupling_term,
            int_dt=self.int_dt)
        return np.copy(self.current_y), np.copy(self.current_yd)

    def open_loop(self, run_t=1.0, coupling_term=None):
        return spring_damper_open_loop(
            self.dt,
            self.start_y, self.goal_y,
            self.k, self.c,
            coupling_term,
            run_t, self.int_dt)


class SpringDamperOrientation:
    def __init__(self, dt=0.01, k=1.0, c=None, int_dt=0.001):
        self.dt = dt
        self.k = k
        self.c = c
        self.int_dt = int_dt

        self.last_t = None
        self.t = 0.0
        self.start_y = np.zeros(4)
        self.start_yd = np.zeros(3)
        self.start_ydd = np.zeros(3)
        self.goal_y = np.zeros(4)
        self.initialized = False
        self.current_y = np.zeros(4)
        self.current_yd = np.zeros(3)
        self.configure()

    def configure(self, last_t=None, t=None, start_y=None, start_yd=None, start_ydd=None, goal_y=None):
        if last_t is not None:
            self.last_t = last_t
        if t is not None:
            self.t = t
        if start_y is not None:
            self.start_y = start_y
        if start_yd is not None:
            self.start_yd = start_yd
        if start_ydd is not None:
            self.start_ydd = start_ydd
        if goal_y is not None:
            self.goal_y = goal_y

    def step(self, last_y, last_yd, coupling_term=None):
        self.last_t = self.t
        self.t += self.dt

        if not self.initialized:
            self.current_y = np.copy(self.start_y)
            self.current_yd = np.copy(self.start_yd)
            self.initialized = True

        self.current_y[:], self.current_yd[:] = spring_damper_step_quaternion(
            self.last_t, self.t,
            last_y, last_yd,
            self.goal_y,
            self.k, self.c,
            coupling_term=coupling_term,
            int_dt=self.int_dt)
        return np.copy(self.current_y), np.copy(self.current_yd)

    def open_loop(self, run_t=1.0, coupling_term=None):
        return spring_damper_open_loop_quaternion(
            self.dt,
            self.start_y, self.goal_y,
            self.k, self.c,
            coupling_term,
            run_t, self.int_dt)


def spring_damper_step(last_t, t, last_y, last_yd, goal_y, k=1.0, c=None, coupling_term=None, coupling_term_precomputed=None, int_dt=0.001):
    if c is None:  # set for critical damping
        c = 2.0 * np.sqrt(k)

    y = np.copy(last_y)
    yd = np.copy(last_yd)

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd, cdd = coupling_term.coupling(y)
        else:
            cd, cdd = np.zeros_like(y), np.zeros_like(y)
        if coupling_term_precomputed is not None:
            cd += coupling_term_precomputed[0]
            cdd += coupling_term_precomputed[1]

        ydd = k * (goal_y - y) - c * yd
        yd += dt * ydd + cd
        y += dt * yd
    return y, yd


def spring_damper_step_quaternion(last_t, t, last_y, last_yd, goal_y, k=1.0, c=None, coupling_term=None, coupling_term_precomputed=None, int_dt=0.001):
    if c is None:  # set for critical damping
        c = 2.0 * np.sqrt(k)

    y = np.copy(last_y)
    yd = np.copy(last_yd)

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd, cdd = coupling_term.coupling(y)
        else:
            cd, cdd = np.zeros(3), np.zeros(3)
        if coupling_term_precomputed is not None:
            cd += coupling_term_precomputed[0]
            cdd += coupling_term_precomputed[1]

        ydd = k * pr.compact_axis_angle_from_quaternion(pr.concatenate_quaternions(goal_y, pr.q_conj(y))) - c * yd
        yd += dt * ydd + cd
        y = pr.concatenate_quaternions(pr.quaternion_from_compact_axis_angle(dt * yd), y)
    return y, yd


def spring_damper_open_loop(dt, start_y, goal_y, k=1.0, c=None, coupling_term=None, run_t=1.0, int_dt=0.001):
    t = 0.0
    y = np.copy(start_y)
    yd = np.zeros_like(y)
    T = [t]
    Y = [np.copy(y)]
    while t < run_t:
        last_t = t
        t += dt
        y, yd = spring_damper_step(
            last_t, t, y, yd,
            goal_y=goal_y,
            k=k, c=c, coupling_term=coupling_term, int_dt=int_dt)
        T.append(t)
        Y.append(np.copy(y))
    return np.asarray(T), np.asarray(Y)


def spring_damper_open_loop_quaternion(dt, start_y, goal_y, k=1.0, c=None, coupling_term=None, run_t=1.0, int_dt=0.001):
    t = 0.0
    y = np.copy(start_y)
    yd = np.zeros(3)
    T = [t]
    Y = [np.copy(y)]
    while t < run_t:
        last_t = t
        t += dt
        y, yd = spring_damper_step_quaternion(
            last_t, t, y, yd,
            goal_y=goal_y,
            k=k, c=c, coupling_term=coupling_term, int_dt=int_dt)
        T.append(t)
        Y.append(np.copy(y))
    return np.asarray(T), np.asarray(Y)