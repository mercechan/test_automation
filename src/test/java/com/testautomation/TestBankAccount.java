package com.testautomation;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class TestBankAccount {
    @Test
    public void testFunds() {
        BankAccount account = new BankAccount(10);
        double amount = account.debit(5);
        assertEquals(5.0, amount);
    }
}
