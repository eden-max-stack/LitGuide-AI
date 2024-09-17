// convex/keywords.ts

import { query, mutation, action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

export const listKeywords = query({
    args: {},
    handler: async (ctx) => {
        const allKeywords = await ctx.db.query("keywords").collect();
        return allKeywords;
    },
  });

  export const insertValues = mutation({
    args: { keyword: v.string() },
    handler: async (ctx, { keyword }) => {
      await ctx.db.insert("keywords", { keyword });
    },
  });

  export const deleteData = mutation({
    args: { id: v.id("keywords") },
    handler: async (ctx, args) => {
      await ctx.db.delete(args.id)
    },
  });
